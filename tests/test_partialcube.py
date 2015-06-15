import unittest

from pads.medium import Medium
from pads.medium import BitvectorMedium
from pads.medium import StateTransitionGraph
from pads.partial_cube import MediumForPartialCube
from pads.partial_cube import isPartialCube


class PartialCubeTest(unittest.TestCase):

    # make medium from all five-bit numbers that have 2 or 3 bits lit
    twobits = [3,5,6,9,10,12,17,18,20,24]
    threebits = [31^x for x in twobits]
    M523 = BitvectorMedium(twobits+threebits,5)

    def testIsPartialCube(self):
        M = PartialCubeTest.M523
        G = StateTransitionGraph(M)
        I = isPartialCube(G)
        self.assertEqual(I,True)
    
    def testK4(self):
        G = {i:[j for j in range(4) if j != i] for i in range(4)}
        self.assertEqual(isPartialCube(G),False)

    def testK33(self):
        G = {0:[3,4,5],1:[3,4,5],2:[3,4,5],3:[0,1,2],4:[0,1,2],5:[0,1,2]}
        self.assertEqual(isPartialCube(G),False)

    def testMediumForPartialCube(self):
        """Check that we get an isomorphic medium via MediumForPartialCube."""
        # Note that we do not get the same tokens.
        # So, we need to check equality of graphs
        # rather than equality of media.
        M = PartialCubeTest.M523
        G = StateTransitionGraph(M)
        E = MediumForPartialCube(G)
        H = StateTransitionGraph(E)
        self.assertEqual(set(G),set(H))
        for v in G:
            self.assertEqual(set(G[v]),set(H[v]))

    def test6212(self):
        """
        A graph that can be labeled, but is not a partial cube.
        Tests the code in LabeledGraphMedium that checks for the
        existence of multiple equally labeled edges at a vertex.
        """
        n,a,b,c = 6,2,1,2
        G = {}
        for i in range(n):
            G[i,0] = [(i,1),((i+b)%n,3),((i+c)%n,3)]
            G[i,1] = [(i,0),(i,2),((i-a)%n,2)]
            G[i,2] = [(i,1),(i,3),((i+a)%n,1)]
            G[i,3] = [(i,2),((i-b)%n,0),((i-c)%n,0)]
        self.assertEqual(isPartialCube(G),False)

    def test61150(self):
        """
        Another graph that can be labeled, but is not a partial cube.
        Tests the code in RoutingTable that makes sure that only tokens
        in a single direction belong to the initial list of active tokens.
        """
        G = {}
        n,a,b,c,d = 6,1,1,5,0
        for i in range(n):
            G[i,0] = [(i,1),((i+a)%n,5),((i+b)%n,3)]
            G[i,1] = [(i,0),(i,2),((i-d)%n,4)]
            G[i,2] = [(i,1),(i,3),((i+c)%n,5)]
            G[i,3] = [(i,2),(i,4),((i-b)%n,0)]
            G[i,4] = [(i,3),(i,5),((i+d)%n,1)]
            G[i,5] = [(i,4),((i-a)%n,0),((i-c)%n,2)]
        self.assertEqual(isPartialCube(G),False)
