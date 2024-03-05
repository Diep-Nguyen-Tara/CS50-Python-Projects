import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Get filenames from command-line arguments
    database_filename = sys.argv[1]
    sequence_filename = sys.argv[2]

    # Read the DNA sequence file into a variable
    with open(sequence_filename, "r") as sequence_file:
        dna_sequence = sequence_file.read()

    # Read the DNA database file into a variable
    with open(database_filename, "r") as database_file:
        database = list(csv.DictReader(database_file))

    # Check the DNA sequence for matching profiles
    match = find_match(database, dna_sequence)

    if match:
        print(match)
    else:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in the sequence for the most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within the sequence
        # If a match, move substring to the next potential match in the sequence
        # Continue moving the substring and checking for matches until out of consecutive matches
        while True:
            # Adjust the substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            # If there is no match in the substring
            else:
                break

        # Update the most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in the sequence, return the longest run found
    return longest_run


def find_match(database, dna_sequence):
    # Initialize a dictionary to store STR counts from the DNA sequence
    str_counts = {}

    # Iterate through each individual's profile in the database
    for individual in database:
        name = individual["name"]
        match = True

        # Check each STR in the database profile
        for str_name in individual.keys():
            if str_name != "name":
                str_count = int(individual[str_name])
                actual_count = longest_match(dna_sequence, str_name)

                if actual_count != str_count:
                    match = False
                    break
                str_counts[str_name] = actual_count

        # If all STRs match, return the name of the matching individual
        if match:
            return name

    # If no match is found, return None
    return None


if __name__ == "__main__":
    main()
