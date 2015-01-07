import unittest

from pads.LongestIncreasingSubsequence import LongestIncreasingSubsequence

# If run as "python LongestIncreasingSubsequence.py", run tests on various
# small lists and check that the correct subsequences are generated.

class LISTest(unittest.TestCase):
    def testLIS(self):
        self.assertEqual(LongestIncreasingSubsequence([]),[])
        self.assertEqual(LongestIncreasingSubsequence(range(10,0,-1)),[1])
        self.assertEqual(LongestIncreasingSubsequence(range(10)),
                                                      list(range(10)))
        self.assertEqual(LongestIncreasingSubsequence([3,1,4,1,5,9,2,6,5,3,5,8,9,7,9]),
                                                      [1,2,3,5,8,9])

if __name__ == "__main__":
    unittest.main()   
