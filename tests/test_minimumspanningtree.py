import unittest

from pads.minimum_spanning_tree import MinimumSpanningTree


class MSTTest(unittest.TestCase):
    def testMST(self):
        """Check that MinimumSpanningTree returns the correct answer."""
        G = {0:{1:11,2:13,3:12},1:{0:11,3:14},2:{0:13,3:10},3:{0:12,1:14,2:10}}
        T = [(2,3),(0,1),(0,3)]
        for e,f in zip(MinimumSpanningTree(G),T):
            self.assertEqual(min(e),min(f))
            self.assertEqual(max(e),max(f))
