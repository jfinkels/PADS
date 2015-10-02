import unittest

from pads.longest_increasing_subsequence import longest_increasing_subsequence


class LISTest(unittest.TestCase):
    def testLIS(self):
        self.assertEqual(longest_increasing_subsequence([]),[])
        self.assertEqual(longest_increasing_subsequence(range(10,0,-1)),[1])
        self.assertEqual(longest_increasing_subsequence(range(10)),
                                                      list(range(10)))
        self.assertEqual(longest_increasing_subsequence([3,1,4,1,5,9,2,6,5,3,5,8,9,7,9]),
                                                      [1,2,3,5,8,9])
