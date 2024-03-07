from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from functools import wraps
from flask import redirect
import sqlite3
import requests

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Custom function for apologies
def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", message=message), code

# Custom filter
app.jinja_env.filters["usd"] = lambda value: f"${value:,.2f}"

app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Database setup
DATABASE = 'finance.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def get_user_by_username(username):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

def lookup(symbol):
    """Look up quote for symbol."""
    try:
        response = requests.get(f"https://api.iex.cloud/v1/data/core/quote/{symbol}?token=sk_42660b87250c4ba2ac489020857af82c")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    portfolio = []
    grand_total = 0

    with get_db_connection() as conn:
        user_cash = conn.execute('SELECT cash FROM users WHERE id = ?', (user_id,)).fetchone()['cash']
        grand_total += user_cash

        stocks = conn.execute('SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0', (user_id,)).fetchall()

        for stock in stocks:
            stock_info = lookup(stock['symbol'])
            if stock_info:
                total_value = stock_info['price'] * stock['total_shares']
                grand_total += total_value
                portfolio.append({'symbol': stock['symbol'], 'shares': stock['total_shares'], 'price': stock_info['price'], 'total': total_value})

    return render_template('index.html', cash=user_cash, portfolio=portfolio, grand_total=grand_total)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username or not password or not confirmation:
            return apology("Must provide username and password", 400)

        if password != confirmation:
            return apology("Passwords do not match", 400)

        # Check if username already exists
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", (username,))
        if existing_user:
            return apology("Username already exists", 400)

        # Hash the user's password
        hashed_password = generate_password_hash(password)

        # Check if username already exists and insert the new user
        try:
            result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)
            if not result:
                return apology("Username already exists", 400)

            # Remember which user has logged in
            session["user_id"] = result

            flash("Registered successfully! Please log in.")
            return redirect("/")

        except Exception as e:
            print(f"Error registering user: {e}")
            return apology("An error occurred. Please try again.", 500)

    else:
        return render_template("register.html")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()  # Convert symbol to uppercase

        if not symbol:
            return apology("Must provide a stock symbol", 400)

        stock = lookup(symbol)

        if stock is None:
            return apology("Invalid stock symbol", 400)

        return render_template("quoted.html", stock=stock)

    else:
        return render_template("quote.html")

@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    if request.method == 'POST':
        symbol = request.form.get('symbol').upper()
        shares = request.form.get('shares')

        if not symbol:
            return apology("Must provide a stock symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("Shares must be a positive integer", 400)

        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock symbol", 400)

        user_id = session.get('user_id')
        with get_db_connection() as conn:
            user = conn.execute('SELECT cash FROM users WHERE id = ?', (user_id,)).fetchone()
            if not user or user['cash'] < stock['price'] * shares:
                return apology("Not enough cash to complete the purchase", 400)

            conn.execute('UPDATE users SET cash = cash - ? WHERE id = ?', (stock['price'] * shares, user_id))
            conn.execute('INSERT INTO transactions (user_id, symbol, shares, price, transacted) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)', (user_id, symbol, shares, stock['price']))
            conn.commit()

        flash("Purchased successfully!")
        return redirect('/')
    else:
        return render_template("buy.html")


@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    if request.method == 'POST':
        symbol = request.form.get('symbol').upper()
        shares_to_sell = int(request.form.get('shares'))

        with get_db_connection() as conn:
            rows = conn.execute('SELECT shares FROM transactions WHERE user_id = ? AND symbol = ?', (user_id, symbol,)).fetchall()
            shares_owned = sum([row['shares'] for row in rows])

            if shares_to_sell > shares_owned:
                flash("Not enough shares.")
                return redirect('/sell')

            stock = lookup(symbol)
            conn.execute('INSERT INTO transactions (user_id, symbol, shares, price, transacted) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)',
                         (user_id, symbol, -shares_to_sell, stock['price']))
            conn.execute('UPDATE users SET cash = cash + ? WHERE id = ?', (stock['price'] * shares_to_sell, user_id))
            conn.commit()

        return redirect('/')
    else:
        with get_db_connection() as conn:
            symbols = conn.execute('SELECT DISTINCT symbol FROM transactions WHERE user_id = ?', (user_id,)).fetchall()
        return render_template('sell.html', symbols=symbols)

if __name__ == '__main__':
    app.run(debug=True)
