"""GraphDegeneracy.py

Compute the degeneracy of graphs, and degeneracy orderings of graphs.

D. Eppstein, July 2016.
"""
from .graphs import is_undirected
from .bucketqueue import BucketQueue


def degeneracySequence(G):
    """Generate pairs (vertex,number of later neighbors) in degeneracy order.

    """
    if not is_undirected(G):
        raise TypeError("Graph must be undirected")
    Q = BucketQueue()
    for v in G:
        Q[v] = len(G[v])    # prioritize vertices by degree
    for v, d in Q.items():
        yield v, d           # output vertices in priority order
        for w in G[v]:
            if w in Q:
                Q[w] -= 1   # one fewer remaining neighbor


def degeneracy(G):
    """Calculate the degeneracy of a given graph"""
    return max(d for v, d in degeneracySequence(G))


def degeneracyOrientation(G):
    """Directed version of G with <= degeneracy out-neighbors per vertex."""
    D = {}
    for v, d in degeneracySequence(G):
        D[v] = {w for w in G[v] if w not in D}
    return D


def core(G, k=None):
    """The k-core of G, or the deepest core if k is not given.
    The return value is a set of vertices; use Graphs.InducedSubgraph
    if the edges are also needed."""
    level = 0
    coreset = set()
    for v, d in degeneracySequence(G):
        if d > level:                   # new depth record?
            if k is None or level < k:  # we care about new records?
                coreset = set()         # yes, restart core
                level = d
        coreset.add(v)
    return coreset


def triangles(G):
    """Use degeneracy to list all the triangles in G"""
    G = degeneracyOrientation(G)
    return ((u, v, w) for u in G for v in G[u] for w in G[u] if w in G[v])
