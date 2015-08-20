"""PartialCube.py

Test whether a graph is an isometric subgraph of a hypercube.

D. Eppstein, September 2005, rewritten May 2007 per arxiv:0705.1025.
"""

from .bfs import breadth_first_levels
from .medium import MediumError
from .medium import LabeledGraphMedium
from .medium import RoutingTable
from .medium import HypercubeEmbedding
from .bipartite import is_bipartite
from .union_find import UnionFind
from .strong_connectivity import StronglyConnectedComponents
from .graphs import is_undirected


def PartialCubeEdgeLabeling(G):
    """
    Label edges of G by their equivalence classes in a partial cube structure.

    We follow the algorithm of arxiv:0705.1025, in which a number of
    equivalence classes equal to the maximum degree of G can be found
    simultaneously by a single breadth first search, using bitvectors.
    However, in order to avoid deep recursions (problematic in Python)
    we use a union-find data structure to keep track of edge identifications
    discovered so far. That is, we repeatedly contract our initial graph,
    maintaining as we do the property that G[v][w] points to a union-find
    set representing edges in the original graph that have been contracted
    to the single edge v-w.
    """

    # Some simple sanity checks
    if not is_undirected(G):
        raise MediumError("graph is not undirected")
    L = list(StronglyConnectedComponents(G))
    if len(L) != 1:
        raise MediumError("graph is not connected")

    # Set up data structures for algorithm:
    # - UF: union find data structure representing known edge equivalences
    # - CG: contracted graph at current stage of algorithm
    # - LL: limit on number of remaining available labels
    UF = UnionFind()
    CG = {v: {w: (v, w) for w in G[v]} for v in G}
    NL = len(CG) - 1

    # Initial sanity check: are there few enough edges?
    # Needed so that we don't try to use union-find on a dense
    # graph and incur superquadratic runtimes.
    n = len(CG)
    m = sum([len(CG[v]) for v in CG])
    if 1 << (m // n) > n:
        raise MediumError("graph has too many edges")

    # Main contraction loop in place of the original algorithm's recursion
    while len(CG) > 1:
        if not is_bipartite(CG):
            raise MediumError("graph is not bipartite")

        # Find max degree vertex in G, and update label limit
        deg, root = max([(len(CG[v]), v) for v in CG])
        if deg > NL:
            raise MediumError("graph has too many equivalence classes")
        NL -= deg

        # Set up bitvectors on vertices
        bitvec = {v: 0 for v in CG}
        neighbors = {}
        i = 0
        for neighbor in CG[root]:
            bitvec[neighbor] = 1 << i
            neighbors[1 << i] = neighbor
            i += 1

        # Breadth first search to propagate bitvectors to the rest of the graph
        for LG in breadth_first_levels(CG, root):
            for v in LG:
                for w in LG[v]:
                    bitvec[w] |= bitvec[v]

        # Make graph of labeled edges and union them together
        labeled = {v: set() for v in CG}
        for v in CG:
            for w in CG[v]:
                diff = bitvec[v] ^ bitvec[w]
                if not diff or bitvec[w] & ~ bitvec[v] == 0:
                    continue    # zero edge or wrong direction
                if diff not in neighbors:
                    raise MediumError("multiply-labeled edge")
                neighbor = neighbors[diff]
                UF.union(CG[v][w], CG[root][neighbor])
                UF.union(CG[w][v], CG[neighbor][root])
                labeled[v].add(w)
                labeled[w].add(v)

        # Map vertices to components of labeled-edge graph
        component = {}
        compnum = 0
        for SCC in StronglyConnectedComponents(labeled):
            for v in SCC:
                component[v] = compnum
            compnum += 1

        # generate new compressed subgraph
        NG = {i: {} for i in range(compnum)}
        for v in CG:
            for w in CG[v]:
                if bitvec[v] == bitvec[w]:
                    vi = component[v]
                    wi = component[w]
                    if vi == wi:
                        raise MediumError("self-loop in contracted graph")
                    if wi in NG[vi]:
                        UF.union(NG[vi][wi], CG[v][w])
                    else:
                        NG[vi][wi] = CG[v][w]

        CG = NG

    # Here with all edge equivalence classes represented by UF.
    # Turn them into a labeled graph and return it.
    return {v: {w: UF[v, w] for w in G[v]} for v in G}


def MediumForPartialCube(G):
    """
    Find a medium corresponding to the partial cube G.
    Raises MediumError if G is not a partial cube.
    Uses the O(n^2) time algorithm of arxiv:0705.1025.
    """
    L = PartialCubeEdgeLabeling(G)
    M = LabeledGraphMedium(L)
    RoutingTable(M)   # verification step per arxiv:0705.1025
    return M


def PartialCubeLabeling(G):
    """Return vertex labels with Hamming distance = graph distance."""
    return HypercubeEmbedding(MediumForPartialCube(G))


def isPartialCube(G):
    """Test whether the given graph is a partial cube."""
    try:
        MediumForPartialCube(G)
        return True
    except MediumError:
        return False
