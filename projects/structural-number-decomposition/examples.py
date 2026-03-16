from snd import structural_number_decomposition, pretty_print_result


def run_examples():
    """
    Test the Structural Number Decomposition algorithm
    on several example numbers.
    """

    test_numbers = [
        6,
        10,
        12,
        13.3,
        22.7,
        31.5,
        100,
        3.1416
    ]

    for x in test_numbers:
        print("\n")
        result = structural_number_decomposition(x)
        pretty_print_result(result)


if __name__ == "__main__":
    run_examples()
