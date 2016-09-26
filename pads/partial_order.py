"""PartialOrder.py

Various operations on partial orders and directed acyclic graphs.

D. Eppstein, July 2006.
"""

from .dfs import preorder, postorder
from .bipartite_matching import matching


def isTopologicalOrder(G, L):
    """Check that L is a topological ordering of directed graph G."""
    vnum = {}
    for i in range(len(L)):
        if L[i] not in G:
            return False
        vnum[L[i]] = i
    for v in G:
        if v not in vnum:
            return False
        for w in G[v]:
            if w not in vnum or vnum[w] <= vnum[v]:
                return False
    return True


def TopologicalOrder(G):
    """Find a topological ordering of directed graph G."""
    L = list(postorder(G))
    L.reverse()
    if not isTopologicalOrder(G, L):
        raise ValueError("TopologicalOrder: graph is not acyclic.")
    return L


def isAcyclic(G):
    """Return True if G is a directed acyclic graph, False otherwise."""
    L = list(postorder(G))
    L.reverse()
    return isTopologicalOrder(G, L)


def TransitiveClosure(G):
    """
    The transitive closure of graph G.
    This is a graph on the same vertex set containing an edge (v,w)
    whenever v != w and there is a directed path from v to w in G.
    """
    TC = {v: set(preorder(G, v)) for v in G}
    for v in G:
        TC[v].remove(v)
    return TC


def TracePaths(G):
    """
    Turn a DAG with indegree and outdegree <= 1 into a sequence of lists.
    """
    L = []
    for v in TopologicalOrder(G):
        if L and v not in G[L[-1]]:
            yield L
            L = []
        L.append(v)
    if L:
        yield L


def MinimumPathDecomposition(G):
    """
    Cover a directed acyclic graph with a minimum number of paths.
    """
    M, A, B = matching(G)
    H = {v: [] for v in G}
    for v in G:
        if v in M:
            H[M[v]] = (v,)
    return TracePaths(H)


def MinimumChainDecomposition(G):
    """
    Cover a partial order with a minimum number of chains.
    By Dilworth's theorem the number of chains equals the size
    of the largest antichain of the order. The input should be
    a directed acyclic graph, not necessarily transitively closed.
    """
    return MinimumPathDecomposition(TransitiveClosure(G))


def MaximumAntichain(G):
    """
    Find a maximum antichain in the given directed acyclic graph.
    """
    if not isAcyclic(G):
        raise ValueError("MaximumAntichain: input is not acyclic.")
    M, A, B = matching(TransitiveClosure(G))
    return set(A).intersection(B)
