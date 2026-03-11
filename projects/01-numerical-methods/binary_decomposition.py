"""
Mathematical idea

Any positive number can be written as

    x = m * 2^k

where

    1 <= m < 2
    k is an integer

This representation is the binary equivalent of scientific notation.

It is also the foundation of floating-point representation (IEEE-754),
where numbers are stored as:

    sign * mantissa * 2^exponent

This decomposition is useful for computing logarithms because:

    log2(x) = log2(m) + k

and m is always in the small interval:

    1 <= m < 2
"""

def binary_decomposition(x):
    """
    Decompose a positive number as:

        x = m * 2^k

    where:
        1 <= m < 2
        k is an integer

    This is the binary equivalent of scientific notation.
    """

    if x <= 0:
        raise ValueError("The number must be positive")

    m = x
    k = 0

    while m >= 2:
        m /= 2
        k += 1

    while m < 1:
        m *= 2
        k -= 1

    return m, k


if __name__ == "__main__":

    x = float(input("Enter a number: "))

    m, k = binary_decomposition(x)

    print("\nNormalized binary decomposition")
    print("--------------------------------")
    print(f"{x} = {m} * 2^{k}")