"""Bipartite.py

Two-color graphs and find related structures.
D. Eppstein, May 2004.
"""

from .biconnectivity import BiconnectedComponents
from .graphs import union
from .dfs import search as dfs_search
from .dfs import nontree as NONTREE
from .dfs import forward as FORWARD


class NonBipartite(Exception):
    pass


def two_color(G):
    """
    Find a bipartition of G, if one exists.
    Raises NonBipartite or returns dict mapping vertices
    to two colors (True and False).
    """
    color = {}
    for v, w, edgetype in dfs_search(G):
        if edgetype is FORWARD:
            color[w] = not color.get(v, False)
        elif edgetype is NONTREE and color[v] == color[w]:
            raise NonBipartite
    return color


def bipartition(G):
    """
    Find a bipartition of G, if one exists.
    Raises NonBipartite or returns sequence of vertices
    on one side of the bipartition.
    """
    color = two_color(G)
    for v in color:
        if color[v]:
            yield v


def is_bipartite(G):
    """
    Return True if G is bipartite, False otherwise.
    """
    try:
        two_color(G)
        return True
    except NonBipartite:
        return False


def bipartite_orientation(G, adjacency_list_type=set):
    """
    Given an undirected bipartite graph G, return a directed graph in which
    the edges are oriented from one side of the bipartition to the other.
    The second argument has the same meaning as in Graphs.copyGraph.
    """
    B = bipartition(G)
    return {v: adjacency_list_type(iter(G[v])) for v in B}


def odd_core(G):
    """
    Subgraph of vertices and edges that participate in odd cycles.
    Aka, the union of nonbipartite biconnected components.
    """
    return union(*[C for C in BiconnectedComponents(G)
                   if not is_bipartite(C)])
