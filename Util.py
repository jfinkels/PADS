"""Util.py

Simple utility functions for PADS library.
D. Eppstein, April 2004.
"""

def arbitrary_item(S):
    """
    Select an arbitrary item from set or sequence S.
    Avoids bugs caused by directly calling iter(S).next() and
    mysteriously terminating loops in callers' code when S is empty.
    """
    try:
        return iter(S).next()
    except StopIteration:
        raise IndexError("No items to select.")
