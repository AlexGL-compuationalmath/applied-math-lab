import math_utils


def main():
    print("Testing math utilities")

    user_input = input("Enter a number: ")  # Introduce un número

    ok, number = math_utils.parse_float(user_input)

    if not ok:
        print("Invalid input. Please enter a numeric value.")  # Entrada no válida
        return

    print("Square:", math_utils.square(number))
    print("Cube:", math_utils.cube(number))


if __name__ == "__main__":
    main()

