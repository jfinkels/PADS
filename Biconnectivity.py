"""Biconnectivity.py

DFS-based algorithm for computing biconnected components.

D. Eppstein, April 2004.
"""

import unittest
from Graphs import isUndirected
from Util import arbitrary_item
from sets import Set

def BiconnectedComponents(G):
    """
    Generate the biconnected components of G.  G should be represented in
    such a way that "for v in G" loops through the vertices, and "G[v]"
    produces a list of the neighbors of v; for instance, G may be a
    dictionary mapping each vertex to its neighbor set.
    The output is a list of subgraphs of G.
    """
    if not isUndirected(G):
        raise ValueError("BiconnectedComponents: input not undirected graph")

    dfsnumber = {}
    components = []
    ancestors = {}    # DIRECTED subgraph from nodes to DFS ancestors
    disconnected = object() # flag for component without articulation point

    def make_component(start=0, articulation_point=disconnected):
        """Make a new component, removing all active vertices from start onward."""
        component = {}
        if articulation_point is not disconnected:
            component[articulation_point] = Set()
        for v in active[start:]:
            component[v] = Set()
            for w in ancestors[v]:
                component[v].add(w)
                component[w].add(v)
        del active[start:]
        components.append(component)

    def traverse(v):
        """Perform depth-first traversal from v and return its low number."""
        low_v = dfsnumber[v] = len(dfsnumber)
        active.append(v)
        ancestors[v] = Set()
        activelen = len(active)
        for w in G[v]:
            if w in dfsnumber:
                if dfsnumber[w] < dfsnumber[v]:
                    low_v = min(low_v, dfsnumber[w])
                    ancestors[v].add(w)
            else:
                low_w = traverse(w)
                if low_w == dfsnumber[v]:
                    make_component(activelen,v)
                else:
                    low_v = min(low_v,low_w)
                    activelen = len(active)
        return low_v

    for v in G:
        if v not in dfsnumber:
            active = []
            traverse(v)
            if len(active) > 1 or len(G[v]) == 0:
                make_component()

    return components

class NotBiconnected(Exception): pass

def isBiconnected(G):
    """Return True if graph G is biconnected, False otherwise."""

    dfsnumber = {}
    def traverse(v):
        """Stripped down version of DFS from BiconnectedComponents."""
        low_v = dfsnumber[v] = len(dfsnumber)
        for w in G[v]:
            if w in dfsnumber:
                low_v = min(low_v, dfsnumber[w])
            else:
                low_w = traverse(w)
                if low_w == dfsnumber[v] and dfsnumber[w] > 1:
                    raise NotBiconnected
                else:
                    low_v = min(low_v,low_w)
        return low_v

    try:
        traverse(arbitrary_item(G))
    except NotBiconnected:
        return False

    for v in G:
        if v not in dfsnumber:
            return False

    return True
    
    
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
        CV = [component.keys() for component in C]
        for comp in CV:
            comp.sort()
        CV.sort()
        self.assertEqual(CV,[[0,2,5],[1,3,6,8],[2,3],[4,7]])

if __name__ == "__main__":
    unittest.main()   