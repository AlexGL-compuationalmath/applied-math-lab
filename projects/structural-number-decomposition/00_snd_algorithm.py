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


def relative_error(reference: float, approx: float) -> float:
    """
    Relative error between a reference value and an approximation.
    """
    if reference == 0:
        return 0.0
    return abs(reference - approx) / abs(reference)


def absolute_error(reference: float, approx: float) -> float:
    """
    Absolute error between a reference value and an approximation.
    """
    return abs(reference - approx)


def complexity(p: int, q: int) -> int:
    """
    Symbolic complexity measure for a rational p/q.
    Lower is simpler.
    """
    return p + q


def continued_fraction(x: float, max_terms: int = 20) -> list[int]:
    """
    Compute the continued fraction expansion of x.
    """
    if x <= 0:
        raise ValueError("continued_fraction requires x > 0")

    terms = []
    value = x

    for _ in range(max_terms):
        a = math.floor(value)
        terms.append(a)

        frac_part = value - a
        if abs(frac_part) < 1e-14:
            break

        value = 1.0 / frac_part

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


def generate_rational_candidates_bruteforce(
    max_denominator: int,
) -> list[tuple[int, int]]:
    """
    Generate rational candidates p/q in [1, 2).
    Includes all reduced and non-reduced forms; duplicates are removed later.
    """
    candidates = []

    for q in range(1, max_denominator + 1):
        for p in range(q, 2 * q):
            candidates.append((p, q))

    return candidates


def generate_candidates(
    m: float,
    method: str = "hybrid",
    max_terms: int = 20,
    max_denominator: int = 500,
) -> tuple[list[tuple[int, int]], list[int]]:
    """
    Generate candidate rational approximations for mantissa m.

    method:
    - "cf": continued fraction convergents only
    - "bruteforce": all p/q with q <= max_denominator and 1 <= p/q < 2
    - "hybrid": combine both
    """
    method = method.lower().strip()
    cf_terms: list[int] = []
    candidate_set: set[tuple[int, int]] = set()

    if method not in {"cf", "bruteforce", "hybrid"}:
        raise ValueError("method must be 'cf', 'bruteforce', or 'hybrid'")

    if method in {"cf", "hybrid"}:
        cf_terms = continued_fraction(m, max_terms=max_terms)
        convergents = convergents_from_cf(cf_terms)
        for p, q in convergents:
            if q != 0 and 1 <= p / q < 2 and q <= max_denominator:
                candidate_set.add((p, q))

    if method in {"bruteforce", "hybrid"}:
        for p, q in generate_rational_candidates_bruteforce(max_denominator):
            candidate_set.add((p, q))

    candidates = sorted(candidate_set, key=lambda frac: (frac[1], frac[0]))
    return candidates, cf_terms


def choose_mode_parameters(mode: str) -> dict:
    """
    Return default parameters depending on mode.
    """
    mode = mode.lower().strip()

    if mode == "simple":
        return {
            "alpha": 0.92,
            "beta": 0.08,
            "max_denominator": 60,
            "max_terms": 20,
            "max_relative_error_allowed": 0.02,  # 2%
            "method": "hybrid",
        }

    if mode == "accurate":
        return {
            "alpha": 0.995,
            "beta": 0.005,
            "max_denominator": 1000,
            "max_terms": 30,
            "max_relative_error_allowed": 0.001,  # 0.1%
            "method": "hybrid",
        }

    raise ValueError("mode must be 'simple' or 'accurate'")


def structural_number_decomposition(
    x: float,
    mode: str = "simple",
    alpha: float | None = None,
    beta: float | None = None,
    max_terms: int | None = None,
    max_denominator: int | None = None,
    max_relative_error_allowed: float | None = None,
    method: str | None = None,
) -> dict:
    """
    Structural Number Decomposition (SND).

    Represents x > 0 as:
        x = m * 2^k

    Then finds a rational approximation:
        m ≈ p / q

    using a score that balances:
    - numerical accuracy
    - symbolic simplicity

    Parameters can be controlled directly, or derived automatically from:
        mode = "simple" or "accurate"
    """
    if x <= 0:
        raise ValueError("x must be a positive real number")

    defaults = choose_mode_parameters(mode)

    if alpha is None:
        alpha = defaults["alpha"]
    if beta is None:
        beta = defaults["beta"]
    if max_terms is None:
        max_terms = defaults["max_terms"]
    if max_denominator is None:
        max_denominator = defaults["max_denominator"]
    if max_relative_error_allowed is None:
        max_relative_error_allowed = defaults["max_relative_error_allowed"]
    if method is None:
        method = defaults["method"]

    if alpha < 0 or beta < 0:
        raise ValueError("alpha and beta must be non-negative")

    if alpha == 0 and beta == 0:
        raise ValueError("alpha and beta cannot both be zero")

    k, m = binary_normalize(x)
    candidates, cf_terms = generate_candidates(
        m=m,
        method=method,
        max_terms=max_terms,
        max_denominator=max_denominator,
    )

    if not candidates:
        raise ValueError("No valid candidates were generated")

    best_any = None
    best_within_threshold = None

    for p, q in candidates:
        r = p / q

        if not (1 <= r < 2):
            continue

        approx_value = r * (2 ** k)

        rel_err_mantissa = relative_error(m, r)
        rel_err_value = relative_error(x, approx_value)
        abs_err_value = absolute_error(x, approx_value)

        comp = complexity(p, q)
        comp_norm = comp / (2 * max_denominator)

        score = alpha * rel_err_mantissa + beta * comp_norm

        result = {
            "x": x,
            "mode": mode,
            "method": method,
            "k": k,
            "mantissa": m,
            "continued_fraction": cf_terms,
            "p": p,
            "q": q,
            "candidate": r,
            "relative_error_mantissa": rel_err_mantissa,
            "relative_error_value": rel_err_value,
            "absolute_error_value": abs_err_value,
            "complexity": comp,
            "score": score,
            "exact_form": f"{m:.12f} * 2^{k}",
            "structural_form": f"({p}/{q}) * 2^{k}",
            "expanded_numerator": p * (2 ** k),
            "expanded_denominator": q,
            "expanded_fraction": f"{p * (2 ** k)}/{q}",
            "approx_value": approx_value,
        }

        if best_any is None or score < best_any["score"]:
            best_any = result

        if rel_err_value <= max_relative_error_allowed:
            if best_within_threshold is None or score < best_within_threshold["score"]:
                best_within_threshold = result

    final_result = best_within_threshold if best_within_threshold is not None else best_any

    if final_result is None:
        raise ValueError("The algorithm failed to produce a valid result")

    final_result["used_threshold_filter"] = best_within_threshold is not None
    final_result["max_relative_error_allowed"] = max_relative_error_allowed

    return final_result


def pretty_print_result(result: dict) -> None:
    """
    Print the SND result in a readable format.
    """
    print("\nStructural Number Decomposition")
    print("-" * 60)
    print(f"x                         = {result['x']}")
    print(f"mode                      = {result['mode']}")
    print(f"method                    = {result['method']}")
    print(f"binary exponent (k)       = {result['k']}")
    print(f"mantissa (m)              = {result['mantissa']:.12f}")

    if result["continued_fraction"]:
        print(f"continued fraction        = {result['continued_fraction']}")
    else:
        print("continued fraction        = []")

    print(f"best fraction             = {result['p']}/{result['q']}")
    print(f"candidate value           = {result['candidate']:.12f}")
    print(f"structural form           = {result['structural_form']}")
    print(f"expanded fraction         = {result['expanded_fraction']}")
    print(f"approximate value         = {result['approx_value']:.12f}")
    print(f"absolute error            = {result['absolute_error_value']:.12f}")
    print(f"relative error            = {result['relative_error_value']:.12f}")
    print(f"relative error (%)        = {100 * result['relative_error_value']:.8f}%")
    print(f"complexity                = {result['complexity']}")
    print(f"score                     = {result['score']:.12f}")
    print(f"threshold used            = {result['used_threshold_filter']}")
    print(f"max allowed rel. error    = {result['max_relative_error_allowed']:.12f}")

    print("\nFinal summary")
    print("-" * 60)
    print(
        f"{result['x']} ≈ {result['structural_form']} = {result['approx_value']:.12f}"
    )
    print(f"Equivalent rational form: {result['expanded_fraction']}")
    print(f"Absolute error:           {result['absolute_error_value']:.12f}")
    print(f"Relative error:           {result['relative_error_value']:.12f}")
    print(f"Relative error (%):       {100 * result['relative_error_value']:.8f}%")


def ask_mode() -> str:
    """
    Ask the user which mode to use.
    """
    while True:
        mode = input("Choose mode ['simple' / 'accurate'] (default: simple): ").strip().lower()

        if mode == "":
            return "simple"
        if mode in {"simple", "accurate"}:
            return mode

        print("Invalid mode. Please type 'simple' or 'accurate'.")


def main() -> None:
    """
    Interactive loop for testing many numbers.
    """
    print("Structural Number Decomposition (SND)")
    print("-" * 60)
    print("Type a positive real number to analyze it.")
    print("Type 'q' to quit.\n")

    while True:
        user_input = input("Enter number: ").strip()

        if user_input.lower() in {"q", "quit", "exit"}:
            print("Goodbye")
            break

        try:
            x = float(user_input)
            if x <= 0:
                print("Please enter a positive real number.\n")
                continue

            mode = ask_mode()

            result = structural_number_decomposition(x=x, mode=mode)
            pretty_print_result(result)
            print()

        except ValueError as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()