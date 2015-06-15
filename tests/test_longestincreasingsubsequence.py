import unittest

from pads.longest_increasing_subsequence import LongestIncreasingSubsequence


class LISTest(unittest.TestCase):
    def testLIS(self):
        self.assertEqual(LongestIncreasingSubsequence([]),[])
        self.assertEqual(LongestIncreasingSubsequence(range(10,0,-1)),[1])
        self.assertEqual(LongestIncreasingSubsequence(range(10)),
                                                      list(range(10)))
        self.assertEqual(LongestIncreasingSubsequence([3,1,4,1,5,9,2,6,5,3,5,8,9,7,9]),
                                                      [1,2,3,5,8,9])
