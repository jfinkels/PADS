import unittest

from pads.integerpoints import IntegerPointsByDistance


class IntegerPointsByDistanceTest(unittest.TestCase):
    radius = 100
    threshold = radius**2
    trange = range(-radius,radius+1)

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
