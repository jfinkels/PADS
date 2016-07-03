"""IntegerPoints.py

Efficient streaming algorithms to generate all integer points (x,y)
of the Euclidean plane, in order by distance from the origin.

D. Eppstein, July 2016.
"""

import unittest
from BucketQueue import BucketQueue

def PositiveIntegerPointsByDistance():
    """List the 2d integer points in order by distance from the origin.
    To avoid repetition, we only list pairs (x,y)
    where x and y are non-negative integers with y <= x."""
    Q = BucketQueue()
    Q[0,0] = 0
    for x,y in Q:
        yield x,y
        Q[x+1,y] = (x+1)**2 + y**2
        if x == y:
            Q[x+1,x+1] = 2*(x+1)**2

def IntegerPointsByDistance():
    """All integer points in order by distance, regardless of sign.
    The space needed to generate the first N points is O(sqrt N).
    Because the priorities used are monotonic and O(N), the
    total time to generate the first N points is also O(N)."""
    for x,y in PositiveIntegerPointsByDistance():
        yield x,y
        if x != 0:
            yield -x,y
            if y != 0:
                yield x,-y
                yield -x,-y
            if x != y:
                yield y,x
                yield y,-x
                if y != 0:
                    yield -y,x
                    yield -y,-x


# ============================================================
#     If run from command line, perform unit tests
# ============================================================

class IntegerPointsByDistanceTest(unittest.TestCase):
    threshold = 100
    trange = range(-10,11)

    def testOrdered(self):
        """Test whether point ordering is by distance."""
        oldDistance = 0
        for x,y in IntegerPointsByDistance():
            newDistance = x**2 + y**2
            self.assertTrue(newDistance >= oldDistance)
            oldDistance = newDistance
            if newDistance > IntegerPointsByDistanceTest.threshold:
                break

    def testCircle(self):
        """Test whether each point in a disk is listed exactly once."""
        points = []
        for x,y in IntegerPointsByDistance():
            if x**2 + y**2 > IntegerPointsByDistanceTest.threshold:
                break
            points.append((x,y))
        self.assertEqual(len(points),len(set(points)))
        self.assertEqual(len(points),len(
            [None for x in IntegerPointsByDistanceTest.trange
             for y in IntegerPointsByDistanceTest.trange
             if x**2 + y**2 <= IntegerPointsByDistanceTest.threshold]))

if __name__ == "__main__":
    unittest.main()   
