people = {
    "Carter": "+1-715-256-2910",
    "David": "+1-345-134-1000"
}

name = input("Name: ")
if name in people:
    number = people[name]
    print(f"Number: {number}")
