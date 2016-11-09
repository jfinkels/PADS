import unittest

from pads.partial_order import isAcyclic
from pads.partial_order import TransitiveClosure
from pads.partial_order import MaximumAntichain
from pads.partial_order import MinimumChainDecomposition


class PartialOrderTest(unittest.TestCase):
    cube = {i:[i^b for b in (1,2,4,8) if i^b > i] for i in range(16)}
            
    def testHypercubeAcyclic(self):
        self.assertTrue(isAcyclic(self.cube))
        
    def testHypercubeClosure(self):
        TC = TransitiveClosure(self.cube)
        for i in range(16):
            self.assertEqual(TC[i],
                {j for j in range(16) if i & j == i and i != j})

    def testHypercubeAntichain(self):        
        A = MaximumAntichain(self.cube)
        self.assertEqual(A,{3,5,6,9,10,12})
        
    def testHypercubeDilworth(self):
        CD = list(MinimumChainDecomposition(self.cube))
        self.assertEqual(len(CD),6)
