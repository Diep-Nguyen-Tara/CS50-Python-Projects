import cs50


# Function to calculate the Coleman-Liau index
def calculate_index(letters, words, sentences):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    return round(index)


# Prompt the user for input
text = cs50.get_string("Text: ")

# Initialize counters
letters, words, sentences = 0, 1, 0

# Count letters, words, and sentences
for char in text:
    if char.isalpha():
        letters += 1
    elif char.isspace():
        words += 1
    elif char in [".", "!", "?"]:
        sentences += 1

# Calculate the Coleman-Liau index
index = calculate_index(letters, words, sentences)

# Print the result
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
