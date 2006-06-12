"""xyzGraph.py

Eventually, code to recognize xyz graphs will go here.
For now, just listing all the ways of partitioning a graph into three matchings.

D. Eppstein, June 2006.
"""

from Graphs import isUndirected
from TopologicalOrder import TopologicalOrder
from Biconnectivity import stOrientation
from sets import Set
import unittest

def CubicMatchPartitions(G):
    """Partition a biconnected cubic graph G into three matchings.
    Each matching is represented as a graph, in which G[v] is a list
    of the three edges of G in the order of the three matchings.
    This function generates a sequence of such representations.
    """
    
    if not isUndirected(G):
        raise ValueError("CubicMatchPartitions: graph is not undirected")
    for v in G:
        if len(G[v]) != 3:
            raise ValueError("CubicMatchPartitions: graph is not cubic")
    ST = stOrientation(G)
    L = TopologicalOrder(ST)
    for B in xrange(1L<<(len(L)//2 - 1)):
        # Here with a bitstring representing the sequence of choices
        out = {}
        pos = 0
        for v in L:
            source = [w for w in G[v] if w in out]
            sourcepos = {}
            adjlist = [None,None,None]
            for w in source:
                sourcepos[w] = [i for i in (0,1,2) if out[w][i]==v][0]
                adjlist[sourcepos[w]] = w
            usedpos = [sourcepos[w] for w in source]
            if len(Set(usedpos)) != len(usedpos):
                # two edges in with same index, doesn't form matching
                break 
            elif len(source) == 0:
                # start vertex, choose one orientation
                adjlist = list(ST[v])
            elif len(source) == 1:
                # two outgoing vertices, one incoming
                avail = [i for i in (0,1,2) if i != usedpos[0]]
                if B & (1L<<pos):
                    avail.reverse()
                pos += 1
                for i,w in zip(avail,list(ST[v])):
                    adjlist[i] = w
            elif len(source) == 2:
                avail = 3 - sum(usedpos)
                adjlist[avail] = list(ST[v])[0]
            out[v] = adjlist
            if len(source) == 3:
                # final vertex of topological ordering, still all consistent
                yield out

class xyzGraphTest(unittest.TestCase):
    cube = dict([(v,[v^i for i in (1,2,4)]) for v in range(8)])
    def testCubicMatchPartitions(self):
        self.assertEqual(len(list(CubicMatchPartitions(self.cube))),4)

if __name__ == "__main__":
    unittest.main()   
