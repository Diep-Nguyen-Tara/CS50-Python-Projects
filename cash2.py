from cs50 import get_float

# Prompt the user for the amount of change owed, re-prompting if it's not non-negative
while True:
    dollars = get_float("Change owed: ")
    if dollars >= 0:
        break

# Convert dollars to cents
cents = round(dollars * 100)

# Initialize variables to keep track of the number of coins used
quarters = 0
dimes = 0
nickels = 0
pennies = 0

# Calculate the minimum number of coins
while cents > 0:
    if cents >= 25:
        quarters += 1
        cents -= 25
    elif cents >= 10:
        dimes += 1
        cents -= 10
    elif cents >= 5:
        nickels += 1
        cents -= 5
    else:
        pennies += 1
        cents -= 1

# Print the total number of coins required
total_coins = quarters + dimes + nickels + pennies
print(total_coins)
