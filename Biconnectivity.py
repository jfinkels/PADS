"""Biconnectivity.py

DFS-based algorithm for computing biconnected components.

D. Eppstein, April 2004.
"""

from Graphs import isUndirected

def BiconnectedComponents(G):
    """
    Generate the biconnected components of G.  G should be represented in
    such a way that "for v in G" loops through the vertices, and "G[v]"
    produces a list of the neighbors of v; for instance, G may be a
    dictionary mapping each vertex to its neighbor set.
    The output is a sequence of lists of vertices of G.
    """
    if not isUndirected(G):
        raise ValueError("BiconnectedComponents: input not undirected graph")

    dfsnumber = {}
    low = {}
    components = []

    def traverse(v):
        desclow = low[v] = dfsnumber[v] = len(dfsnumber)
        active.append(v)
        activelen = len(active)
        for w in G[v]:
            if w in dfsnumber:
                low[v] = min(low[v], dfsnumber[w])
            else:
                traverse(w)
                if low[w] == dfsnumber[v]:
                    components.append(active[activelen:])
                    components[-1].append(v)
                    del active[activelen:]
                else:
                    low[v] = min(low[v],low[w])
                    activelen = len(active)

    for v in G:
        if v not in dfsnumber:
            active = []
            traverse(v)
            if len(active) > 1 or len(G[v]) == 0:
                components.append(active)

    return components

def isBiconnected(G):
    """Return True if graph G is biconnected, False otherwise."""
    return len(BiconnectedComponents(G)) == 1
