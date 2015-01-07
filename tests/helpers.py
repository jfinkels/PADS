def neq_(a, b, msg=None):
    """Shorthand for ``assert a != b, "%r == %r" % (a, b)``."""
    if a == b:
        raise AssertionError(msg or "%r == %r" % (a, b))
