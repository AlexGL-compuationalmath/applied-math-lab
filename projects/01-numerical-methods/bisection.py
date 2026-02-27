def bisection(f, a, b, tol=1e-8, max_iter=100, verbose=True):
    fa = f(a)
    fb = f(b)

    if fa * fb >= 0:
        raise ValueError("Function must change sign on [a, b].")

    for i in range(1, max_iter + 1):
        m = (a + b) / 2
        fm = f(m)

        if verbose:
            width = abs(b - a)
            print(f"iter {i:02d} | a={a:.10f} b={b:.10f} m={m:.10f} | f(m)={fm:.3e} | width={width:.3e}")

        # Stop if f(m) is close enough to 0 OR interval is small enough
        if abs(fm) < tol or abs(b - a) < tol:
            return m

        # Keep the half-interval that contains the sign change
        if fa * fm < 0:
            b = m
            fb = fm
        else:
            a = m
            fa = fm

    print("Stopped: did not converge within max_iter.")
    return m


def f(x):
    return x**2 - 2


def main():
    root = bisection(f, a=1, b=2)
    print("\nApproximate root:", root)


if __name__ == "__main__":
    main()