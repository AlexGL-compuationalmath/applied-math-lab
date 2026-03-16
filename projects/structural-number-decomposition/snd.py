import math


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


def absolute_error(x: float, approx: float) -> float:
    """
    Absolute error between the original number and its approximation.
    """
    return abs(x - approx)


def complexity(p: int, q: int) -> int:
    """
    Simple symbolic complexity measure.
    """
    return p + q


def continued_fraction(x: float, max_terms: int = 12) -> list[int]:
    """
    Compute the continued fraction expansion of x.
    """
    terms = []
    value = x

    for _ in range(max_terms):
        a = math.floor(value)
        terms.append(a)

        frac_part = value - a
        if abs(frac_part) < 1e-12:
            break

        value = 1 / frac_part

    return terms


def convergents_from_cf(cf: list[int]) -> list[tuple[int, int]]:
    """
    Compute convergents from a continued fraction expansion.
    Returns a list of (p, q).
    """
    convergents = []

    p_minus2, p_minus1 = 0, 1
    q_minus2, q_minus1 = 1, 0

    for a in cf:
        p = a * p_minus1 + p_minus2
        q = a * q_minus1 + q_minus2

        convergents.append((p, q))

        p_minus2, p_minus1 = p_minus1, p
        q_minus2, q_minus1 = q_minus1, q

    return convergents


def structural_number_decomposition(
    x: float,
    max_terms: int = 12,
    max_denominator: int = 100,
    alpha: float = 0.85,
    beta: float = 0.15,
) -> dict:
    """
    Structural Number Decomposition (SND), based on continued fractions.

    Represents x > 0 as:
        x = m * 2^k

    Then searches for a simple rational approximation of m
    using convergents from its continued fraction expansion.

    Returns a dictionary with the best structural representation.
    """
    if x <= 0:
        raise ValueError("x must be a positive real number")

    if alpha < 0 or beta < 0:
        raise ValueError("alpha and beta must be non-negative")

    if alpha == 0 and beta == 0:
        raise ValueError("alpha and beta cannot both be zero")

    k, m = binary_normalize(x)

    cf = continued_fraction(m, max_terms=max_terms)
    convergents = convergents_from_cf(cf)

    candidates = []
    for p, q in convergents:
        if q == 0:
            continue

        r = p / q
        if 1 <= r < 2 and q <= max_denominator:
            candidates.append((p, q))

    if not candidates:
        raise ValueError("No valid candidates were generated")

    best_result = None

    for p, q in candidates:
        r = p / q
        approx_value = r * (2 ** k)

        rel_err = relative_error(m, r)
        abs_err = absolute_error(x, approx_value)
        comp = complexity(p, q)
        comp_norm = comp / (2 * max_denominator if max_denominator > 0 else 1)

        score = alpha * rel_err + beta * comp_norm

        if best_result is None or score < best_result["score"]:
            best_result = {
                "x": x,
                "k": k,
                "mantissa": m,
                "continued_fraction": cf,
                "p": p,
                "q": q,
                "candidate": r,
                "relative_error": rel_err,
                "absolute_error": abs_err,
                "complexity": comp,
                "score": score,
                "exact_form": f"{m:.10f} * 2^{k}",
                "structural_form": f"({p}/{q}) * 2^{k}",
                "approx_value": approx_value,
            }

    return best_result


def pretty_print_result(result: dict) -> None:
    """
    Print the SND result in a readable form.
    """
    print("\nStructural Number Decomposition")
    print("-" * 50)
    print(f"x                      = {result['x']}")
    print(f"binary exponent (k)    = {result['k']}")
    print(f"mantissa (m)           = {result['mantissa']:.10f}")
    print(f"continued fraction     = {result['continued_fraction']}")
    print(f"best fraction          = {result['p']}/{result['q']}")
    print(f"candidate value        = {result['candidate']:.10f}")
    print(f"structural form        = {result['structural_form']}")
    print(f"approximate value      = {result['approx_value']:.10f}")
    print(f"relative error         = {result['relative_error']:.10f}")
    print(f"absolute error         = {result['absolute_error']:.10f}")
    print(f"complexity             = {result['complexity']}")
    print(f"score                  = {result['score']:.10f}")

    print("\nFinal summary")
    print("-" * 50)
    print(f"{result['x']} ≈ {result['structural_form']}")
    print(f"Approximate value: {result['approx_value']:.10f}")
    print(f"Relative error:   {result['relative_error']:.10f}")
    print(f"Absolute error:   {result['absolute_error']:.10f}")


def main() -> None:
    """
    Ask the user for a positive number and run the algorithm.
    """
    print("Structural Number Decomposition (SND)")
    print("-" * 50)

    user_input = input("Enter a positive real number: ").strip()

    try:
        x = float(user_input)
        result = structural_number_decomposition(x)
        pretty_print_result(result)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
   
