import unittest

from pads.bipartite import isBipartite


class BipartitenessTest(unittest.TestCase):
    def cycle(self,n):
        return {i:[(i-1)%n,(i+1)%n] for i in range(n)}

    def testEvenCycles(self):
        for i in range(4,12,2):
            self.assertEqual(isBipartite(self.cycle(i)), True)

    def testOddCycles(self):
        for i in range(3,12,2):
            self.assertEqual(isBipartite(self.cycle(i)), False)
