import unittest

from pads.acyclic_reachability import Reachability


class ReachabilityTest(unittest.TestCase):
    def testReachable(self):
        G = {"A":["C"],"B":["C","D"],"C":["D","E"],"D":[],"E":[]}
        R = Reachability(G)
        for s in "ABCDE":
            for t in "ABCDE":
                self.assertEqual(R.reachable(s,t),
                                 s <= t and s+t not in ["AB","DE"])
