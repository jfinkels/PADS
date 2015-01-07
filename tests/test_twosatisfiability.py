import unittest

from pads.TwoSatisfiability import Forced
from pads.TwoSatisfiability import Not
from pads.TwoSatisfiability import Satisfiable

# Unit tests
# Run python TwoSatisfiability.py to perform these tests.

class TwoSatTest(unittest.TestCase):
    T1 = {1:[2,3], 2:[Not(1),3]}
    T2 = {1:[2], 2:[Not(1)], Not(1):[3], 3:[4,2], 4:[1]}

    def testTwoSat(self):
        """Check that the correct problems are satisfiable."""
        self.assertEqual(Satisfiable(self.T1),True)
        self.assertEqual(Satisfiable(self.T2),False)

    def testForced(self):
        """Check that we can correctly identify forced variables."""
        self.assertEqual(Forced(self.T1),{1:False})
        self.assertEqual(Forced(self.T2),None)

if __name__ == "__main__":
    unittest.main()   
