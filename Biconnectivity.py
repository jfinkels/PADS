"""Biconnectivity.py

DFS-based algorithm for computing biconnected components.

D. Eppstein, April 2004.
"""

import unittest
from Graphs import isUndirected
from Util import arbitrary_item
from sets import Set
import DFS

disconnected = object() # flag for BiconnectedComponents

class BiconnectedComponents(DFS.Searcher):
    """
    Generate the biconnected components of G.  G should be represented in
    such a way that "for v in G" loops through the vertices, and "G[v]"
    produces a list of the neighbors of v; for instance, G may be a
    dictionary mapping each vertex to its neighbor set.
    The result of BiconnectedComponents(G) is a sequence of subgraphs of G.
    """
    
    def __init__(self,G):
        """Search for biconnected components of graph G."""
        if not isUndirected(G):
            raise ValueError("BiconnectedComponents: input not undirected graph")
    
        # set up data structures for DFS
        self._components = []
        self._dfsnumber = {}
        self._activelen = {}
        self._active = []
        self._low = {}
        self._ancestors = {} # directed subgraph from nodes to DFS ancestors
        
        # perform the Depth First Search
        DFS.Searcher.__init__(self,G)
        
        # clean up now-useless data structures
        del self._dfsnumber, self._activelen, self._active
        del self._low, self._ancestors

    def __iter__(self):
        """Return iterator for sequence of biconnected components."""
        return iter(self._components)

    def preorder(self,parent,child):
        if parent == child:
            self._active = [child]
        else:
            self._active.append(child)
        self._low[child] = self._dfsnumber[child] = len(self._dfsnumber)
        self._ancestors[child] = Set()
        self._activelen[child] = len(self._active)

    def backedge(self,source,destination):
        if self._dfsnumber[destination] < self._dfsnumber[source]:
            self._low[source] = min(self._low[source],
                                    self._dfsnumber[destination])
            self._ancestors[source].add(destination)

    def postorder(self,parent,child):
        if parent == child:
            if not self._components or child not in self._components[-1]:
                self._component()
        elif self._low[child] == self._dfsnumber[parent]:
            self._component(self._activelen[parent],parent)
        else:
            self._low[parent] = min(self._low[parent],self._low[child])
            self._activelen[parent] = len(self._active)

    def _component(self,start=0, articulation_point=disconnected):
        """Make new component, removing active vertices from start onward."""
        component = {}
        if articulation_point is not disconnected:
            component[articulation_point] = Set()
        for v in self._active[start:]:
            component[v] = Set()
            for w in self._ancestors[v]:
                component[v].add(w)
                component[w].add(v)
        del self._active[start:]
        self._components.append(component)


class NotBiconnected(Exception): pass

class BiconnectivityTester(DFS.Searcher):
    """
    Stripped down version of BiconnectedComponents.
    Either successfully inits or raises NotBiconnected.
    Otherwise does nothing.
    """
    
    def __init__(self,G):
        """Search for biconnected components of graph G."""
        if not isUndirected(G):
            raise ValueError("BiconnectedComponents: input not undirected graph") 
        self._dfsnumber = {}
        self._low = {}
        self._rootedge = None
        DFS.Searcher.__init__(self,G)

    def preorder(self,parent,child):
        if parent == child and self._rootedge:
            raise NotBiconnected    # two roots, not even connected
        elif not self._rootedge and parent != child:
            self._rootedge = (parent,child)
        self._low[child] = self._dfsnumber[child] = len(self._dfsnumber)

    def backedge(self,source,destination):
        self._low[source] = min(self._low[source],self._dfsnumber[destination])

    def postorder(self,parent,child):
        if parent == child:
            if not self._rootedge:  # flag start from isolated vertex
                self._rootedge = parent,child
        elif self._low[child] != self._dfsnumber[parent]:
            self._low[parent] = min(self._low[parent],self._low[child])
        elif (parent,child) != self._rootedge:
            raise NotBiconnected    # articulation point


def isBiconnected(G):
    """Return True if graph G is biconnected, False otherwise."""
    try:
        BiconnectivityTester(G)
        return True
    except NotBiconnected:
        return False

    
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
        self.assertEqual(isBiconnected(self.G1), True)
        self.assertEqual(isBiconnected(self.G2), False)
        
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