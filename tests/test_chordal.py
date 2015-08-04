import unittest

from pads.chordal import is_chordal
from pads.chordal import perfect_elimination_ordering


class ChordalTest(unittest.TestCase):
    claw = {0:[1,2,3],1:[0],2:[0],3:[0]}
    butterfly = {0:[1,2,3,4],1:[0,2],2:[0,1],3:[0,4],4:[0,3]}
    diamond = {0:[1,2],1:[0,2,3],2:[0,1,3],3:[1,2]}
    quad = {0:[1,3],1:[0,2],2:[1,3],3:[0,2]}
    graphs = [(claw,True), (butterfly,True), (diamond,True), (quad,False)]
    
    def testChordal(self):
        """Check that Chordal() returns the correct answer on each test graph."""
        for G,isChordal in ChordalTest.graphs:
            self.assertEqual(is_chordal(G), isChordal)

    def testElimination(self):
        """Check that PerfectEliminationOrdering generates an elimination ordering."""
        for G,isChordal in ChordalTest.graphs:
            if isChordal:
                eliminated = set()
                for v in perfect_elimination_ordering(G):
                    eliminated.add(v)
                    for w in G[v]:
                        for x in G[v]:
                            if w != x and w not in eliminated and x not in eliminated:
                                self.assertTrue(w in G[x] and x in G[w]) 
