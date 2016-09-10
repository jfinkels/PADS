import unittest

from pads.halin import is_D3_reducible
from pads.halin import hamiltonian_cycle_D3
from pads.halin import halin_leaf_vertices
from pads.halin import is_wheel
from pads.halin import is_dual_3_tree
from pads.halin import is_halin


class TestHalin(unittest.TestCase):
    cube = {i:[i^1,i^2,i^4] for i in range(8)}
    trunctet = {(i,j):[(i,k) for k in range(4) if k!=i and k!=j]+[(j,i)]
                for i in range(4) for j in range(4) if i!=j}
    wheel = {0:[1,2,3,4,5],1:[0,2,5],2:[0,1,3],3:[0,2,4],4:[0,3,5],5:[0,1,4]}
    halin8 = {0:[1,7,5],1:[0,2,7],2:[1,3,6],3:[2,4,6],
              4:[3,5,6],5:[0,4,6],6:[2,3,4,5,7],7:[0,1,6]}
    nonhalin = {0:[1,2,4],1:[0,3,5,7],2:[0,3,4,6],3:[1,2,7],
                4:[0,2,6],5:[1,6,7],6:[2,4,5],7:[1,3,5]}
    ternary = {0:(1,2,3),13:(4,14,39),39:(12,13,38)}
    for i in range(1,13):
        ternary[i] = ((i-1)//3,3*i+1,3*i+2,3*i+3)
    for i in range(14,39):
        ternary[i] = ((i-1)//3,i-1,i+1)

    def test_is_D3_reducible(self):
        """Check correct classification of D3-reducible graphs"""
        self.assertEqual(is_D3_reducible(self.cube), False)
        self.assertEqual(is_D3_reducible(self.trunctet), True)
        self.assertEqual(is_D3_reducible(self.wheel), True)
        self.assertEqual(is_D3_reducible(self.nonhalin), True)
        self.assertEqual(is_D3_reducible(self.ternary), True)

    def test_reduction_types(self):
        """Check that the correct reduction types are being applied"""
        self.assertEqual(is_wheel(self.trunctet),False)
        self.assertEqual(is_wheel(self.wheel),True)
        self.assertEqual(is_wheel(self.ternary),False)
        self.assertEqual(is_wheel(self.nonhalin), False)
        self.assertEqual(is_dual_3_tree(self.trunctet),True)
        self.assertEqual(is_dual_3_tree(self.wheel),False)
        self.assertEqual(is_dual_3_tree(self.ternary),False)
        self.assertEqual(is_dual_3_tree(self.nonhalin), False)

    def test_halin(self):
        """Check correct classification of Halin graphs"""
        self.assertEqual(is_halin(self.cube), False)
        self.assertEqual(is_halin(self.trunctet), False)
        self.assertEqual(is_halin(self.wheel), True)
        self.assertEqual(is_halin(self.halin8), True)
        self.assertEqual(is_halin(self.nonhalin), False)
        self.assertEqual(is_halin(self.ternary), True)
        self.assertEqual(halin_leaf_vertices(self.wheel),{1,2,3,4,5})
        self.assertEqual(halin_leaf_vertices(self.halin8),{0,1,2,3,4,5})
        self.assertEqual(halin_leaf_vertices(self.ternary),set(range(13,40)))

    def test_hamiltonian(self):
        """Check correct construction of Hamiltonian cycle"""
        for G in (self.trunctet,self.wheel,self.nonhalin,self.ternary):
            H = hamiltonian_cycle_D3(G)
            self.assertEqual(set(H),set(G))     # same vertices?
            for v in H:
                self.assertEqual(len(H[v]),2)   # degree-two?
                for w in H[v]:
                    self.assertEqual(w in G[v], True)   # subgraph?
