import random
import unittest

from pads.integer_heap import IntegerHeap
from pads.integer_heap import LinearHeap

random.seed(1234)

class IntegerHeapTest(unittest.TestCase):
    def testHeaps(self):
        o = 5               # do tests on 2^5-bit integers
        N = LinearHeap()
        I = IntegerHeap(o)
        for iteration in range(20000):
            self.assertEqual(bool(N),bool(I))   # both have same emptiness
            if (not N) or random.randrange(2):  # flip coin for add/remove
                x = random.randrange(1<<(1<<o))
                N.add(x)
                I.add(x)
            else:
                x = N.min()
                self.assertEqual(x,I.min())
                N.remove(x)
                I.remove(x)
