"""LexBFS.py

Lexicographic breadth-first-search traversal of a graph, as described
in Habib, McConnell, Paul, and Viennot, "Lex-BFS and Partition Refinement,
with Applications to Transitive Orientation, Interval Graph Recognition,
and Consecutive Ones Testing", Theor. Comput. Sci. 234:59-84 (2000),
http://www.cs.colostate.edu/~rmm/lexbfs.ps

D. Eppstein, November 2003.
"""

from __future__ import generators

from PartitionRefinement import PartitionRefinement
from Sequence import Sequence

def LexBFS(G):
    """Find lexicographic breadth-first-search traversal order of a graph.
    G should be represented in such a way that "for v in G" loops through
    the vertices, and "G[v]" produces a sequence of the neighbors of v; for
    instance, G may be a dictionary mapping each vertex to its neighbor set.
    """
    P = PartitionRefinement(G)
    S = Sequence([iter(P).next()], key=id)
    while S:
        set = iter(S).next()    # find first set in ordered partition
        v = iter(set).next()    # and first remaining vertex in that set
        yield v
        P.remove(v)
        if not set:
            S.remove(set)
        for new,old in P.refine(G[v]):
            S.insertBefore(old,new)
