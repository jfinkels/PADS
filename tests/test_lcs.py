import unittest

from pads.lcs import longest_common_subsequence


class LCSTest(unittest.TestCase):
    def testLCS(self):
        A = range(10)
        B = reversed(A)
        self.assertEqual(list(A), longest_common_subsequence(A, A))
        self.assertEqual(len(longest_common_subsequence(A, B)), 1)
