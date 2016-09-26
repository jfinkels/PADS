import unittest

from pads.biconnectivity import is_biconnected
from pads.biconnectivity import st_orientation
from pads.biconnectivity import BiconnectedComponents
from pads.partial_order import TopologicalOrder


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
        self.assertEqual(is_biconnected(self.G1), True)
        self.assertEqual(is_biconnected(self.G2), False)

    def testBiconnectedComponents(self):
        """G2 has four biconnected components."""
        C = BiconnectedComponents(self.G2)
        CV = sorted(sorted(component.keys()) for component in C)
        self.assertEqual(CV,[[0,2,5],[1,3,6,8],[2,3],[4,7]])
    
    def test_st_orientation(self):
        STO = st_orientation(self.G1)
        L = list(TopologicalOrder(STO))
        indegree = dict([(v,0) for v in self.G1])
        for v in L:
            for w in STO[v]:
                indegree[w] += 1
        outdegree = dict([(v,len(STO[v])) for v in self.G1])
        self.assertEqual(len([v for v in self.G1 if indegree[v] == 0]), 1)
        self.assertEqual(len([v for v in self.G1 if outdegree[v] == 0]), 1)
