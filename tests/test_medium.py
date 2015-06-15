import unittest

from pads.medium import BitvectorMedium
from pads.medium import RoutingTable
from pads.medium import HypercubeEmbedding
from pads.medium import StateTransitionGraph
from pads.medium import ExplicitMedium
from pads.medium import LabeledGraphMedium


class MediumTest(unittest.TestCase):

    # make medium from all five-bit numbers that have 2 or 3 bits lit
    twobits = [3,5,6,9,10,12,17,18,20,24]
    threebits = [31^x for x in twobits]
    M523 = BitvectorMedium(twobits+threebits,5)

    def testStates(self):
        """Check that iter(Medium) generates the correct set of states."""
        M = MediumTest.M523
        L1 = list(M)
        L1.sort()
        L2 = MediumTest.twobits + MediumTest.threebits
        L2.sort()
        self.assertEqual(L1,L2)
    
    def testTokens(self):
        """Check that Medium.tokens() generates the correct set of tokens."""
        M = MediumTest.M523
        toks = [(i,False) for i in range(5)] + [(i,True) for i in range(5)]
        self.assertEqual(set(toks),set(M.tokens()))
        for t in toks:
            i,b = t
            self.assertEqual(M.reverse(t),(i,not b))
    
    def testAction(self):
        """Check that the action of the tokens is what we expect."""
        M = MediumTest.M523
        for x in M:
            for i in range(5):
                b = (x>>i)&1
                self.assertEqual(x,M(x,(i,b)))
                y = M(x,(i,not b))
                if b == (x in MediumTest.twobits):
                    self.assertEqual(x,y)
                else:
                    self.assertEqual(y,x^(1<<i))
    
    def testRouting(self): 
        """Check that RoutingTable finds paths that decrease Hamming dist."""
        M = MediumTest.M523
        R = RoutingTable(M)
        for x in M:
            for y in M:
                if x != y:
                    i,b = R[x,y]
                    self.assertEqual((x^y)&(1<<i),1<<i)
                    self.assertEqual((x>>i)&1, not b)
    
    def testExplicit(self):            
        """Check that ExplicitMedium looks the same as its argument."""
        M = MediumTest.M523
        E = ExplicitMedium(M)
        self.assertEqual(set(M),set(E))
        self.assertEqual(set(M.tokens()),set(E.tokens()))
        for t in M.tokens():
            self.assertEqual(M.reverse(t),E.reverse(t))
        for s in M:
            for t in M.tokens():
                self.assertEqual(M(s,t),E(s,t))

    def testEmbed(self):
        """Check that HypercubeEmbedding finds appropriate coordinates."""
        M = MediumTest.M523
        E = HypercubeEmbedding(M)
        def ham(x,y):
            z = x^y
            d = 0
            while z:
                d += 1
                z &= z-1
            return d
        for x in M:
            for y in M:
                self.assertEqual(ham(x,y),ham(E[x],E[y]))     

    def testGraph(self):
        """Check that LabeledGraphMedium(StateTransitionGraph(M)) = M."""
        M = MediumTest.M523
        L = LabeledGraphMedium(StateTransitionGraph(M))
        self.assertEqual(set(M),set(L))
        self.assertEqual(set(M.tokens()),set(L.tokens()))
        for t in M.tokens():
            self.assertEqual(M.reverse(t),L.reverse(t))
        for s in M:
            for t in M.tokens():
                self.assertEqual(M(s,t),L(s,t))
