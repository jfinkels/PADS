import unittest

from pads.sorted_set import SortedSet

class SortedSetTest(unittest.TestCase):
    def testSortedSet(self):
        """Test whether SortedSet works correctly."""
        S = SortedSet()
        self.assertEqual(len(S),0)
        S.add(1)
        S.add(4)
        S.add(2)
        S.add(9)
        S.add(3)
        self.assertEqual(list(S),[1,2,3,4,9])
        self.assertEqual(len(S),5)
        S.remove(4)
        S.add(6)
        S.add(5)
        S.add(7)
        S.remove(6)
        S.remove(1)
        S.remove(2)
        S.add(1)
        self.assertEqual(list(S),[1,3,5,7,9])
        self.assertEqual(list(SortedSet([1,3,6,7])),[1,3,6,7])
