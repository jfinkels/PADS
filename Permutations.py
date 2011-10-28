"""Permutations.py
Efficient recursive version of the Steinhaus-Johnson-Trotter algorithm
for listing all permutations of a set of items.
D. Eppstein, October 2011.

The algorithm sets up a sequence of recursive simple generators,
each taking constant space, for a total space of O(n), where n is
the number of items being permuted. The number of recursive calls
to generate a swap that moves the item originally in position n
of the input permutation is O(n-i+1), so all but a 1/n fraction of
the swaps take no recursion and the rest always take O(n) time,
for an average time per swap of O(1).
"""

import unittest

def PlainChanges(n):
    """Generate the swaps for the Steinhaus-Johnson-Trotter algorithm."""
    if n < 1:
        return
    up = xrange(n-1)
    down = xrange(n-2,-1,-1)
    recur = PlainChanges(n-1)
    try:
        while True:
            for x in down:
                yield x
            yield recur.next() + 1
            for x in up:
                yield x
            yield recur.next()
    except StopIteration:
        pass

def SteinhausJohnsonTrotter(x):
    """Generate all permutations of x.
    If x is a number rather than an iterable, we generate the permutations
    of range(x)."""

    # set up the permutation and its length
    try:
        perm = list(x)
    except:
        perm = range(x)
    n = len(perm)

    # run through the sequence of swaps
    yield perm
    for x in PlainChanges(n):
        perm[x],perm[x+1] = perm[x+1],perm[x]
        yield perm

def DoublePlainChanges(n):
    """Generate the swaps for double permutations."""
    if n < 1:
        return
    up = xrange(1,2*n-1)
    down = xrange(2*n-2,0,-1)
    recur = DoublePlainChanges(n-1)
    try:
        while True:
            for x in up:
                yield x
            yield recur.next() + 1
            for x in down:
                yield x
            yield recur.next() + 2
    except StopIteration:
        pass

def DoubleSteinhausJohnsonTrotter(n):
    """Generate all double permutations of the range 0 through n-1"""
    perm = []
    for i in range(n):
        perm += [i,i]

    # run through the sequence of swaps
    yield perm
    for x in DoublePlainChanges(n):
        perm[x],perm[x+1] = perm[x+1],perm[x]
        yield perm

# If run standalone, perform unit tests
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
        for L in ([1,3,5,7], list('zyx'), [], [[]], range(20)):
            self.assertEqual(L,SteinhausJohnsonTrotter(L).next())

if __name__ == "__main__":
    unittest.main()
