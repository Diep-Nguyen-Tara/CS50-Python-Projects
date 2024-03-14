def main():
    while True:
        height = get_height()
        if height >= 1 and height <= 8:
            break

    print_pyramid(height)


def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if height >= 1 and height <= 8:
                return height
            else:
                print("Height must be between 1 and 8.")
        except ValueError:
            print("Please enter a valid integer.")


def print_pyramid(height):
    for i in range(height):
        spaces = " " * (height - i - 1)
        blocks = "#" * (i + 1)
        print(spaces + blocks)


if __name__ == "__main__":
    main()
