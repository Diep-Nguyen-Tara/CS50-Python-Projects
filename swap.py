text = "In the great green room"
words = text.split()

print("Round 1")
for word in words:
    print(word, end=" ")
print()

print("Round 2")
for word in words:
    for c in words:
        print(c)
print()
