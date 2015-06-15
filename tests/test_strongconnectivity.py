import unittest

from pads.strong_connectivity import StronglyConnectedComponents
from pads.strong_connectivity import Condensation


class StrongConnectivityTest(unittest.TestCase):

    G1 = { 0:[1], 1:[2,3], 2:[4,5], 3:[4,5], 4:[6], 5:[], 6:[] }
    C1 = [[0],[1],[2],[3],[4],[5],[6]]

    # Work around http://bugs.python.org/issue11796 by using a loop
    # instead of a dict/set comprehension in a class variable initializer
    # should be:
    # Con1 = {frozenset([v]):{frozenset([w]) for w in G1[v]} for v in G1}
    Con1 = {}
    for v in G1:
        Con1[frozenset([v])] = {frozenset([w]) for w in G1[v]}
    
    G2 = { 0:[1], 1:[2,3,4], 2:[0,3], 3:[4], 4:[3] }
    C2 = [[0,1,2],[3,4]]
    f012 = frozenset([0,1,2])
    f34 = frozenset([3,4])
    Con2 = {f012:{f34}, f34:set()}
    
    knownpairs = [(G1,C1),(G2,C2)]

    def testStronglyConnectedComponents(self):
        """Check known graph/component pairs."""
        for (graph,expectedoutput) in self.knownpairs:
            output = [list(C) for C in StronglyConnectedComponents(graph)]
            for component in output:
                component.sort()
            output.sort()
            self.assertEqual(output,expectedoutput)

    def testSubgraph(self):
        """Check that each SCC is an induced subgraph."""
        for (graph,expectedoutput) in self.knownpairs:
            components = StronglyConnectedComponents(graph)
            for C in components:
                for v in C:
                    for w in graph:
                        self.assertEqual(w in graph[v] and w in C, w in C[v])

    def testCondensation(self):
        """Check that the condensations are what we expect."""
        self.assertEqual(Condensation(self.G1),self.Con1)
        self.assertEqual(Condensation(self.G2),self.Con2)
