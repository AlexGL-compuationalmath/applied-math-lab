import math
from fractions import Fraction


def binary_normalize(x: float) -> tuple[int, float]:
    """
    Decompose x > 0 as x = m * 2^k with 1 <= m < 2.
    Returns (k, m).
    """
    if x <= 0:
        raise ValueError("x must be a positive real number")

    k = math.floor(math.log2(x))
    m = x / (2 ** k)
    return k, m


def relative_error(m: float, r: float) -> float:
    """
    Relative error between mantissa m and candidate r.
    """
    return abs(m - r) / m


def complexity(p: int, q: int) -> int:
    """
    Simple symbolic complexity measure.
    """
    return p + q


def structural_number_decomposition(
    x: float,
    max_denominator: int = 12,
    alpha: float = 0.85,
    beta: float = 0.15,
) -> dict:
    """
    Structural Number Decomposition (SND)

    Represents x > 0 as:
        x = m * 2^k

    Then searches for a simple rational approximation:
        m ≈ p / q

    using a score that balances:
    - relative error
    - symbolic complexity

    Returns a dictionary with the best structural representation.
    """
    if x <= 0:
        raise ValueError("x must be a positive real number")

    if alpha < 0 or beta < 0:
        raise ValueError("alpha and beta must be non-negative")

    if alpha == 0 and beta == 0:
        raise ValueError("alpha and beta cannot both be zero")

    k, m = binary_normalize(x)

    best_result = None

    # We generate candidate fractions in [1, 2)
    for q in range(1, max_denominator + 1):
        for p in range(q, 2 * q):
            r = p / q

            err = relative_error(m, r)
            comp = complexity(p, q)

            # Normalized complexity
            comp_norm = comp / (3 * max_denominator)

            score = alpha * err + beta * comp_norm

            if best_result is None or score < best_result["score"]:
                best_result = {
                    "x": x,
                    "k": k,
                    "mantissa": m,
                    "p": p,
                    "q": q,
                    "candidate": r,
                    "error": err,
                    "complexity": comp,
                    "score": score,
                    "exact_form": f"{m:.10f} * 2^{k}",
                    "structural_form": f"({p}/{q}) * 2^{k}",
                    "approx_value": r * (2 ** k),
                }

    return best_result


def pretty_print_result(result: dict) -> None:
    """
    Print the SND result in a readable form.
    """
    print("Structural Number Decomposition")
    print("-" * 40)
    print(f"x                = {result['x']}")
    print(f"binary exponent   = {result['k']}")
    print(f"mantissa          = {result['mantissa']:.10f}")
    print(f"best fraction     = {result['p']}/{result['q']}")
    print(f"candidate value   = {result['candidate']:.10f}")
    print(f"approximation     = {result['structural_form']}")
    print(f"approx value      = {result['approx_value']:.10f}")
    print(f"relative error    = {result['error']:.10f}")
    print(f"complexity        = {result['complexity']}")
    print(f"score             = {result['score']:.10f}")


if __name__ == "__main__":
    x = 13.3
    result = structural_number_decomposition(x)
    pretty_print_result(result)
