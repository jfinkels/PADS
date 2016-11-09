import unittest

from pads.integer_partitions import mckay
from pads.integer_partitions import fixed_length_partitions
from pads.integer_partitions import partitions
from pads.integer_partitions import conjugate
from pads.integer_partitions import binary_partitions
from pads.integer_partitions import lex_partitions
from pads.integer_partitions import revlex_partitions


class PartitionTest(unittest.TestCase):
    counts = [1,1,2,3,5,7,11,15,22,30,42,56,77,101,135]

    def testCounts(self):
        """Check that each generator has the right number of outputs."""
        for n in range(len(self.counts)):
            self.assertEqual(self.counts[n],len(list(mckay(n))))
            self.assertEqual(self.counts[n],len(list(lex_partitions(n))))
            self.assertEqual(self.counts[n],len(list(revlex_partitions(n))))

    def testSums(self):
        """Check that all outputs are partitions of the input."""
        for n in range(len(self.counts)):
            for p in mckay(n):
                self.assertEqual(n,sum(p))
            for p in revlex_partitions(n):
                self.assertEqual(n,sum(p))
            for p in lex_partitions(n):
                self.assertEqual(n,sum(p))
    
    def testRevLex(self):
        """Check that the revlex generators' outputs are in revlex order."""
        for n in range(len(self.counts)):
            last = [n+1]
            for p in mckay(n):
                self.assertGreater(last, p)
                last = list(p)  # make less-mutable copy
            last = [n+1]
            for p in revlex_partitions(n):
                self.assertGreater(last, p)
                last = list(p)  # make less-mutable copy

    def testLex(self):
        """Check that the lex generator's outputs are in lex order."""
        for n in range(1,len(self.counts)):
            last = []
            for p in lex_partitions(n):
                self.assertLess(last, p)
                last = list(p)  # make less-mutable copy

    def testRange(self):
        """Check that all numbers in output partitions are in range."""
        for n in range(len(self.counts)):
            for p in mckay(n):
                for x in p:
                    self.assertLess(0, x)
                    self.assertLessEqual(x, n)
            for p in lex_partitions(n):
                for x in p:
                    self.assertLess(0, x)
                    self.assertLessEqual(x, n)
            for p in revlex_partitions(n):
                for x in p:
                    self.assertLess(0, x)
                    self.assertLessEqual(x, n)
    
    def testFixedLength(self):
        """Check that the fixed length partition outputs are correct."""
        for n in range(len(self.counts)):
            pn = [list(p) for p in revlex_partitions(n)]
            pn.sort()
            np = 0
            for L in range(n+1):
                pnL = [list(p) for p in fixed_length_partitions(n,L)]
                pnL.sort()
                np += len(pnL)
                self.assertEqual(pnL,[p for p in pn if len(p) == L])
            self.assertEqual(np,len(pn))
                
    def testConjugatePartition(self):
        """Check that conjugating a partition forms another partition."""
        for n in range(len(self.counts)):
            for p in partitions(n):
                c = conjugate(p)
                for x in c:
                    self.assertLess(0, x)
                    self.assertLessEqual(x, n)
                self.assertEqual(sum(c),n)

    def testConjugateInvolution(self):
        """Check that double conjugation returns the same partition."""
        for n in range(len(self.counts)):
            for p in partitions(n):
                self.assertEqual(p,conjugate(conjugate(p)))

    def testConjugateMaxLen(self):
        """Check the max-length reversing property of conjugation."""
        for n in range(1,len(self.counts)):
            for p in partitions(n):
                self.assertEqual(len(p),max(conjugate(p)))

    def testBinary(self):
        """Test that the binary partitions are generated correctly."""
        for n in range(len(self.counts)):
            binaries = []
            for p in partitions(n):
                for x in p:
                    if x & (x - 1):
                        break
                else:
                    binaries.append(list(p))
            self.assertEqual(binaries,[list(p) for p in binary_partitions(n)])
