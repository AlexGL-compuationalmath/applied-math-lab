def square(x):
    """Return x squared."""
    return x**2


def cube(x):
    """Return x cubed."""
    return x**3


def parse_float(text):
    """
    Try to convert text to float.
    Returns: (ok, value)
      ok: True/False
      value: float if ok else None
    """
    try:
        return True, float(text)
    except ValueError:
        return False, None

