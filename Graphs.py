"""Graphs.py

Various simple functions for graph input.

Each function's input graph G should be represented in such a way that "for v in G" loops through the vertices, and "G[v]" produces a list of the neighbors of v; for instance, G may be a dictionary mapping each vertex to its neighbor set.

D. Eppstein, April 2004.
"""

def isUndirected(G):
    """Check that G represents a simple undirected graph."""
    for v in G:
        if v in G[v]:
            return False
        for w in G[v]:
            if v not in G[w]:
                return False
    return True

def maxDegree(G):
    """Return the maximum vertex (out)degree of graph G."""
    return max([len(G[v]) for v in G])

def minDegree(G):
    """Return the minimum vertex (out)degree of graph G."""
    return min([len(G[v]) for v in G])

def copyGraph(G):
    """Make a copy of a graph G and return the copy."""
    return dict([(v,dict([(w,True) for w in G[v]])) for v in G])
