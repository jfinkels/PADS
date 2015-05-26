import unittest

from pads.halin import D3reducible
from pads.halin import D3HamiltonianCycle
from pads.halin import HalinLeafVertices
from pads.halin import isWheel
from pads.halin import isDual3Tree
from pads.halin import isHalin


class HalinTest(unittest.TestCase):
    cube = {i:[i^1,i^2,i^4] for i in range(8)}
    trunctet = {(i,j):[(i,k) for k in range(4) if k!=i and k!=j]+[(j,i)]
                for i in range(4) for j in range(4) if i!=j}
    wheel = {0:[1,2,3,4,5],1:[0,2,5],2:[0,1,3],3:[0,2,4],4:[0,3,5],5:[0,1,4]}
    nonhalin = {0:[1,2,4],1:[0,3,5,7],2:[0,3,4,6],3:[1,2,7],
                4:[0,2,6],5:[1,6,7],6:[2,4,5],7:[1,3,5]}
    ternary = {0:(1,2,3),13:(4,14,39),39:(12,13,38)}
    for i in range(1,13):
        ternary[i] = ((i-1)//3,3*i+1,3*i+2,3*i+3)
    for i in range(14,39):
        ternary[i] = ((i-1)//3,i-1,i+1)

    def testD3Reducible(self):
        """Check correct classification of D3-reducible graphs"""
        self.assertEqual(D3reducible(self.cube), False)
        self.assertEqual(D3reducible(self.trunctet), True)
        self.assertEqual(D3reducible(self.wheel), True)
        self.assertEqual(D3reducible(self.nonhalin), True)
        self.assertEqual(D3reducible(self.ternary), True)

    def testReductionTypes(self):
        """Check that the correct reduction types are being applied"""
        self.assertEqual(isWheel(self.trunctet),False)
        self.assertEqual(isWheel(self.wheel),True)
        self.assertEqual(isWheel(self.ternary),False)
        self.assertEqual(isWheel(self.nonhalin), False)
        self.assertEqual(isDual3Tree(self.trunctet),True)
        self.assertEqual(isDual3Tree(self.wheel),False)
        self.assertEqual(isDual3Tree(self.ternary),False)
        self.assertEqual(isDual3Tree(self.nonhalin), False)

    def testHalin(self):
        """Check correct classification of Halin graphs"""
        self.assertEqual(isHalin(self.cube), False)
        self.assertEqual(isHalin(self.trunctet), False)
        self.assertEqual(isHalin(self.wheel), True)
        self.assertEqual(isHalin(self.nonhalin), False)
        self.assertEqual(isHalin(self.ternary), True)
        self.assertEqual(HalinLeafVertices(self.wheel),{1,2,3,4,5})
        self.assertEqual(HalinLeafVertices(self.ternary),set(range(13,40)))

    def testHamiltonian(self):
        """Check correct construction of Hamiltonian cycle"""
        for G in (self.trunctet,self.wheel,self.nonhalin,self.ternary):
            H = D3HamiltonianCycle(G)
            self.assertEqual(set(H),set(G))     # same vertices?
            for v in H:
                self.assertEqual(len(H[v]),2)   # degree-two?
                for w in H[v]:
                    self.assertEqual(w in G[v], True)   # subgraph?
