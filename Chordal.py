"""Chordal.py

Recognize and compute elimination ordering of chordal graphs, using
an algorithm from http://www.cs.colostate.edu/~rmm/lexbfs.ps

D. Eppstein, November 2003.
"""

from LexBFS import LexBFS
from sets import Set

def Chordal(G):
    """Return a perfect elimination ordering, or None if G is not chordal.
    G should be represented in such a way that "for v in G" loops through
    the vertices, and "G[v]" produces a list of the neighbors of v; for
    instance, G may be a dictionary mapping each vertex to its neighbor set.
    """
    left = Set()
    B = list(LexBFS(G))
    position = dict([(B[i],i) for i in range(len(B))])
    LN = {}
    parent = {}
    for v in B:
        LN[v] = Set(G[v]) & left
        left.add(v)
        if LN[v]:
            parent[v] = B[max([position[w] for w in LN[v]])]
            if not LN[v] - Set([parent[v]]) <= LN[parent[v]]:
                return None
    B.reverse()
    return B
