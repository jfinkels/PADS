import unittest

from pads.xyz_graph import CubicMatchPartitions
from pads.xyz_graph import xyzEmbeddings

class xyzGraphTest(unittest.TestCase):
    cube = {v:[v^i for i in (1,2,4)] for v in range(8)}

    def testCubicMatchPartitions(self):
        """Check that a cube has the right number of matching partitions."""
        self.assertEqual(len(list(CubicMatchPartitions(self.cube))),4)

    def testCubeIsXYZ(self):
        """Check that a cube is correctly identified as an xyz graph."""
        self.assertEqual(len(list(xyzEmbeddings(self.cube))),1)
