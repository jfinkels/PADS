"""Biconnectivity.py

DFS-based algorithm for computing biconnected components.

D. Eppstein, April 2004.
"""

import unittest
from Graphs import isUndirected
from Util import arbitrary_item

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
    components = []

    def traverse(v):
        """Perform depth-first traversal from v and return its low number."""
        low_v = dfsnumber[v] = len(dfsnumber)
        active.append(v)
        activelen = len(active)
        for w in G[v]:
            if w in dfsnumber:
                low_v = min(low_v, dfsnumber[w])
            else:
                low_w = traverse(w)
                if low_w == dfsnumber[v]:
                    components.append(active[activelen:])
                    components[-1].append(v)
                    del active[activelen:]
                else:
                    low_v = min(low_v,low_w)
                    activelen = len(active)
        return low_v

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
    
# If run as "python CubicHam.py", run tests on various small graphs
# and check that the correct results are obtained.

class BiconnectivityTest(unittest.TestCase):
    G1 = {
        0: [1,2,5],
        1: [0,5],
        2: [0,3,4],
        3: [2,4,5,6],
        4: [2,3,5,6],
        5: [0,1,3,4],
        6: [3,4],
    }
    G2 = {
        0: [2,5],
        1: [3,8],
        2: [0,3,5],
        3: [1,2,6,8],
        4: [7],
        5: [0,2],
        6: [3,8],
        7: [4],
        8: [1,3,6],
    }

    def testIsBiconnected(self):
        """G1 is biconnected but G2 is not."""
        assert isBiconnected(self.G1)
        assert not isBiconnected(self.G2)
        
    def testBiconnectedComponents(self):
        """G2 has four biconnected components."""
        C = BiconnectedComponents(self.G2)
        for comp in C:
            comp.sort()
        C.sort()
        self.assertEqual(C,[[0,2,5],[1,3,6,8],[2,3],[4,7]])

if __name__ == "__main__":
    unittest.main()   