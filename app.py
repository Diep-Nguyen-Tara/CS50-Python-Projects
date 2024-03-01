import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import sqlite3

# Create the Flask application
app = Flask(__name__)

# Define a function to create the birthdays table
def create_table():
    conn = sqlite3.connect("birthdays.db")
    db = conn.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS birthdays (id INTEGER PRIMARY KEY, name TEXT, month TEXT, day INTEGER)")
    conn.commit()
    conn.close()

# Route for both handling GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    # Create the birthdays table if it doesn't exist
    create_table()

    if request.method == 'POST':
        # Process form submission and insert new birthday into the database
        name = request.form.get('name')
        month = request.form.get('month')
        day = request.form.get('day')

        # Insert the new birthday into the database
        conn = sqlite3.connect("birthdays.db")
        db = conn.cursor()
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", (name, month, day))
        conn.commit()
        conn.close()

    # Retrieve all birthdays from the database
    conn = sqlite3.connect("birthdays.db")
    db = conn.cursor()
    db.execute("SELECT * FROM birthdays")
    birthdays = db.fetchall()
    conn.close()

    # Render the index.html template with the birthdays data
    return render_template('index.html', birthdays=birthdays)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

