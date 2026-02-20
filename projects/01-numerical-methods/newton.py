def numerical_derivative_centered(f, x, h=1e-5):
    """Centered finite-difference derivative approximation."""
    return (f(x + h) - f(x - h)) / (2 * h)


def newton_method(f, x0, tol=1e-10, max_iter=50, h=1e-5, verbose=True):
    """
    Newton's method to solve f(x)=0.

    Args:
        f: function
        x0: initial guess
        tol: tolerance for stopping (based on step size)
        max_iter: maximum number of iterations
        h: step for numerical derivative
        verbose: print iteration info

    Returns:
        Approximate root (float) or None if it fails.
    """
    x = x0

    for i in range(1, max_iter + 1):
        fx = f(x)
        dfx = numerical_derivative_centered(f, x, h=h)

        if abs(dfx) < 1e-12:
            print("Stopped: derivative too small.")
            return None

        x_new = x - fx / dfx
        step = abs(x_new - x)

        if verbose:
            print(f"iter {i:02d} | x={x:.12f} | f(x)={fx:.3e} | step={step:.3e}")

        if step < tol:
            return x_new

        x = x_new

    print("Stopped: did not converge within max_iter.")
    return None


# Example function: solve x^2 - 2 = 0  (root = sqrt(2))
def f(x):
    return x**2 - 2


def main():
    root = newton_method(f, x0=1)
    print("\nApproximate root:", root)


if __name__ == "__main__":
    main()