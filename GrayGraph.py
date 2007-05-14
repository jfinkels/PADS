"""GrayGraph.py

The Gray Graph

D. Eppstein, October 2006.
"""

import unittest

GrayGraph = {}
for i in [0,1,2]:
    for j in [0,1,2]:
        GrayGraph[i,j,None] = [(i,j,0),(i,j,1),(i,j,2)]
        GrayGraph[i,None,j] = [(i,0,j),(i,1,j),(i,2,j)]
        GrayGraph[None,i,j] = [(0,i,j),(1,i,j),(2,i,j)]
        for k in [0,1,2]:
            GrayGraph[i,j,k] = [(i,j,None),(i,None,k),(None,j,k)]

# Properties of the Gray Graph

class GrayGraphTest(unittest.TestCase):

    def testBipartite(self):
        """The Gray Graph is bipartite."""
        import Bipartite
        self.assertEqual(Bipartite.isBipartite(GrayGraph),True)

    def testPartialCube(self):
        """The Gray Graph is (sadly) not a partial cube."""
        import PartialCube
        self.assertEqual(PartialCube.isPartialCube(GrayGraph),False)

if __name__ == "__main__":
    unittest.main()
