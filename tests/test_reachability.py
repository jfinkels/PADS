import unittest

from pads.AcyclicReachability import Reachability


class ReachabilityTest(unittest.TestCase):
    def testReachable(self):
        G = {"A":["C"],"B":["C","D"],"C":["D","E"],"D":[],"E":[]}
        R = Reachability(G)
        for s in "ABCDE":
            for t in "ABCDE":
                self.assertEqual(R.reachable(s,t),
                                 s <= t and s+t not in ["AB","DE"])

if __name__ == "__main__":
    unittest.main()   
