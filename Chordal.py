"""Chordal.py

Recognize and compute elimination ordering of chordal graphs, using
an algorithm from Habib, McConnell, Paul, and Viennot, "Lex-BFS and
Partition Refinement, with Applications to Transitive Orientation,
Interval Graph Recognition, and Consecutive Ones Testing", Theor.
Comput. Sci. 234:59-84 (2000), http://www.cs.colostate.edu/~rmm/lexbfs.ps

D. Eppstein, November 2003.
"""

from LexBFS import LexBFS
from sets import Set

def PerfectEliminationOrdering(G):
    """Return a perfect elimination ordering, or None if G is not chordal.
    G should be represented in such a way that "for v in G" loops through
    the vertices, and "G[v]" produces a list of the neighbors of v; for
    instance, G may be a dictionary mapping each vertex to its neighbor set.
    """
    alreadyProcessed = Set()
    B = list(LexBFS(G))
    position = dict([(B[i],i) for i in range(len(B))])
    leftNeighbors = {}
    parent = {}
    for v in B:
        leftNeighbors[v] = Set(G[v]) & alreadyProcessed
        alreadyProcessed.add(v)
        if leftNeighbors[v]:
            parent[v] = B[max([position[w] for w in leftNeighbors[v]])]
            if not leftNeighbors[v] - Set([parent[v]]) <= leftNeighbors[parent[v]]:
                return None
    B.reverse()
    return B
