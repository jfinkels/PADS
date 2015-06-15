import random
import unittest

from pads.lca import RangeMin
from pads.lca import LogarithmicRangeMin
from pads.lca import LCA
from pads.lca import OfflineLCA


class RandomRangeMinTest(unittest.TestCase):
    def testRangeMin(self):
        for trial in range(20):
            data = [random.choice(range(1000000))
                    for i in range(random.randint(1,100))]
            R = RangeMin(data)
            for sample in range(100):
                i = random.randint(0,len(data)-1)
                j = random.randint(i+1,len(data))
                self.assertEqual(R[i:j],min(data[i:j]))


class LCATest(unittest.TestCase):
    parent = {'b':'a','c':'a','d':'a','e':'b','f':'b','g':'f','h':'g','i':'g'}
    lcas = {
        ('a','b'):'a',
        ('b','c'):'a',
        ('c','d'):'a',
        ('d','e'):'a',
        ('e','f'):'b',
        ('e','g'):'b',
        ('e','h'):'b',
        ('c','i'):'a',
        ('a','i'):'a',
        ('f','i'):'f',
    }

    def testLCA(self):
        L = LCA(self.parent)
        for k,v in self.lcas.items():
            self.assertEqual(L(*k),v)

    def testLogLCA(self):
        L = LCA(self.parent, LogarithmicRangeMin)
        for k,v in self.lcas.items():
            self.assertEqual(L(*k),v)

    def testOfflineLCA(self):
        L = OfflineLCA(self.parent, self.lcas.keys())
        for (p,q),v in self.lcas.items():
            self.assertEqual(L[p][q],v)
