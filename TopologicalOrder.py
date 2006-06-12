"""TopologicalOrder.py

Find a topological ordering of a DAG, and test for acyclicity.

D. Eppstein, June 2006.
"""

from DFS import postorder

def isTopologicalOrder(G,L):
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
    if not isTopologicalOrder(G,L):
        raise ValueError("TopologicalOrder: graph is not acyclic.")
    return L

def isAcyclic(G):
    """Return True if G is a directed acyclic graph, False otherwise."""
    L = list(postorder(G))
    L.reverse()
    return isTopologicalOrder(G,L):
