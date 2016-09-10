import unittest

from pads.graphdegeneracy import degeneracy
from pads.graphdegeneracy import core
from pads.graphdegeneracy import triangles


class DegeneracyTest(unittest.TestCase):
    G = {1:[2,5],2:[1,3,5],3:[2,4],4:[3,5,6],5:[1,2,4],6:[4]} #File:6n-graf.svg

    def testDegeneracy(self):
        self.assertEqual(degeneracy(DegeneracyTest.G),2)
    
    def testCore(self):
        self.assertEqual(core(DegeneracyTest.G),{1,2,3,4,5})

    def testTriangles(self):
        T = list(triangles(DegeneracyTest.G))
        self.assertEqual(len(T),1)
        self.assertEqual(set(T[0]),{1,2,5})
