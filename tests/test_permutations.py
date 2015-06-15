import unittest

from pads.permutations import Involutions
from pads.permutations import PlainChanges
from pads.permutations import SteinhausJohnsonTrotter


class PermutationTest(unittest.TestCase):    
    def testChanges(self):
        """Do we get the expected sequence of changes for n=3?"""
        self.assertEqual(list(PlainChanges(3)),[1,0,1,0,1])
    
    def testLengths(self):
        """Are the lengths of the generated sequences factorial?"""
        f = 1
        for i in range(2,7):
            f *= i
            self.assertEqual(f,len(list(SteinhausJohnsonTrotter(i))))
    
    def testDistinct(self):
        """Are all permutations in the sequence different from each other?"""
        for i in range(2,7):
            s = set()
            n = 0
            for x in SteinhausJohnsonTrotter(i):
                s.add(tuple(x))
                n += 1
            self.assertEqual(len(s),n)
    
    def testAdjacent(self):
        """Do consecutive permutations in the sequence differ by a swap?"""
        for i in range(2,7):
            last = None
            for p in SteinhausJohnsonTrotter(i):
                if last:
                    diffs = [j for j in range(i) if p[j] != last[j]]
                    self.assertEqual(len(diffs),2)
                    self.assertEqual(p[diffs[0]],last[diffs[1]])
                    self.assertEqual(p[diffs[1]],last[diffs[0]])
                last = list(p)
    
    def testListInput(self):
        """If given a list as input, is it the first output?"""
        for L in ([1,3,5,7], list('zyx'), [], [[]], list(range(20))):
            self.assertEqual(L,next(SteinhausJohnsonTrotter(L)))

    def testInvolutions(self):
        """Are these involutions and do we have the right number of them?"""
        telephone = [1,1,2,4,10,26,76,232,764]
        for n in range(len(telephone)):
            count = 0
            sorted = list(range(n))
            invs = set()
            for p in Involutions(n):
                self.assertEqual([p[i] for i in p],sorted)
                invs.add(tuple(p))
                count += 1
            self.assertEqual(len(invs),count)
            self.assertEqual(len(invs),telephone[n])
