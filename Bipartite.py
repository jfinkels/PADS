"""Bipartite.py

Two-color graphs and find related structures.
D. Eppstein, May 2004.
"""

from sets import Set
from Biconnectivity import BiconnectedComponents

class NonBipartite(Exception):
    pass

def TwoColor(G):
    """
    Find a bipartition of G, if one exists.
    Raises NonBipartite or returns dict mapping vertices
    to two colors (True and False).
    """   
    def traverse(v,parity):
        """Perform depth-first traversal from v and color it."""
        color[v] = parity
        parity = not parity
        for w in G[v]:
            if w in color:
                if color[w] != parity:
                    raise NonBipartite
            else:
                traverse(w,parity)

    color = {}
    for v in G:
        if v not in color:
            traverse(v,True)
    return color

def Bipartition(G):
    """
    Find a bipartition of G, if one exists.
    Raises NonBipartite or returns sequence of vertices
    on one side of the bipartition.
    """
    color = TwoColor(G)
    for v in color:
        if color[v]:
            yield v

def isBipartite(G):
    """
    Return True if G is bipartite, False otherwise.
    """
    try:
        TwoColor(G)
        return True
    except NonBipartite:
        return False

def BipartiteOrientation(G,adjacency_list_type=Set):
    """
    Given an undirected bipartite graph G, return a directed graph in which
    the edges are oriented from one side of the bipartition to the other.
    The second argument has the same meaning as in Graphs.copyGraph.
    """
    B = Bipartition(G)
    return dict([(v,adjacency_list_type(iter(G[v]))) for v in B])

def OddCore(G):
    """
    Set of vertices that participate in odd cycles.
    Aka, vertices that are part of a nonbipartite biconnected component.
    """
    core = Set()
    for C in BiconnectedComponents(G):
        if not isBipartite(C):
            core.update(C)
    return core
