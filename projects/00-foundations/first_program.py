print(__name__)

# First robust Python program in Applied Math Lab

def square(x):
    return x**2


def main():
    print("Applied Math Lab - Foundations")

    try:
        number = float(input("Enter a number: "))
        result = square(number)

        if number == 0:
            print("Zero is a special case.")
            print("Square:", result)
        else:
            print("Square:", result)

    except ValueError:
        print("Error: Please enter a valid numeric value.")


if __name__ == "__main__":
    main()


