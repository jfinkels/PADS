"""LexBFS.py

Lexicographic breadth-first-search traversal of a graph, as described
in http://www.cs.colostate.edu/~rmm/lexbfs.ps

D. Eppstein, November 2003.
"""

from __future__ import generators

from PartitionRefinement import PartitionRefinement
from Sequence import Sequence

def LexBFS(G):
    """Find lexicographic breadth-first-search traversal order of a graph.
    G should be represented in such a way that "for v in G" loops through
    the vertices, and "G[v]" produces a list of the neighbors of v; for
    instance, G may be a dictionary mapping each vertex to its neighbor set.
    """
    P = PartitionRefinement(G)
    set = iter(P).next()
    ids = {id(set):set}   # complicated by inability of set to belong to dict
    S = Sequence([id(set)])
    while S:
        set = ids[iter(S).next()]
        v = iter(set).next()
        yield v
        P.remove(v)
        if not set:
            S.remove(id(set))
            del ids[id(set)]
        for new,old in P.refine(G[v]):
            S.insertBefore(id(old),id(new))
            ids[id(new)] = new
