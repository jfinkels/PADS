import unittest

from pads.lcs import LongestCommonSubsequence


class LCSTest(unittest.TestCase):
    def testLCS(self):
        A = range(10)
        B = reversed(A)
        self.assertEqual(list(A),LongestCommonSubsequence(A,A))
        self.assertEqual(len(LongestCommonSubsequence(A,B)),1)
