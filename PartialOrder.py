"""PartialOrder.py

Various operations on partial orders and directed acyclic graphs.

D. Eppstein, July 2006.
"""

import unittest
from DFS import preorder,postorder
import BipartiteMatching

try:
    set
except NameError:
    from sets import Set as set

def isTopologicalOrder(G,L):
    """Check that L is a topological ordering of directed graph G."""
    vnum = {}
    for i in range(len(L)):
        if L[i] not in G:
            return False
        vnum[L[i]] = i
    for v in G:
        if v not in vnum:
            return False
        for w in G[v]:
            if w not in vnum or vnum[w] <= vnum[v]:
                return False
    return True

def TopologicalOrder(G):
    """Find a topological ordering of directed graph G."""
    L = list(postorder(G))
    L.reverse()
    if not isTopologicalOrder(G,L):
        raise ValueError("TopologicalOrder: graph is not acyclic.")
    return L

def isAcyclic(G):
    """Return True if G is a directed acyclic graph, False otherwise."""
    L = list(postorder(G))
    L.reverse()
    return isTopologicalOrder(G,L)

def TransitiveClosure(G):
    """
    The transitive closure of graph G.
    This is a graph on the same vertex set containing an edge (v,w)
    whenever v != w and there is a directed path from v to w in G.
    """
    TC = dict([(v,set(preorder(G,v))) for v in G])
    for v in G:
        TC[v].remove(v)
    return TC
    
def MaximumAntichain(G):
    """
    Find a maximum antichain in the given directed acyclic graph.
    """
    if not isAcyclic(G):
        raise ValueError("MaximumAntichain: input is not acyclic.")
    TC = TransitiveClosure(G)
    M,A,B = BipartiteMatching.matching(TransitiveClosure(G))
    return set(A).intersection(B)

class PartialOrderTest(unittest.TestCase):
    cube = dict([(i,[]) for i in range(16)])
    for i in range(16):
        for b in (1,2,4,8):
            cube[min(i,i^b)].append(max(i,i^b))
            
    def testHypercubeAcyclic(self):
        self.assert_(isAcyclic(self.cube))
        
    def testHypercubeClosure(self):
        TC = TransitiveClosure(self.cube)
        for i in range(16):
            self.assertEqual(TC[i],
                set([j for j in range(16) if i & j == i and i != j]))

    def testHypercubeAntichain(self):        
        A = MaximumAntichain(self.cube)
        self.assertEqual(A,set((3,5,6,9,10,12)))

if __name__ == "__main__":
    unittest.main()   
