"""TwoSatisfiability.py

Algorithms for solving 2-satisfiability problems.

All instances should be represented as a directed implication graph in which the vertices represent variables and (via Not.py) their negations.

D. Eppstein, April 2009.
"""

import unittest
from Not import Not,SymbolicNegation
from Graphs import copyGraph
from StrongConnectivity import Condensation
from AcyclicReachability import Reachability

def Symmetrize(G):
    """Expand implication graph to include contrapositive of each implication."""
    H = copyGraph(G)
    for v in G:
        H.setdefault(Not(v),set())  # make sure all negations are included
        for w in G[v]:
            H.setdefault(w,set())   # as well as all implicants
            H.setdefault(Not(w),set()) # and negated implicants
    for v in G:
        for w in G[v]:
            H[Not(w)].add(Not(v))
    return H

def Satisfiable(G):
    """Does this instance have a satisfying assignment?"""
    G = Condensation(Symmetrize(G))
    for C in G:
        for v in C:
            if Not(v) in C:
                return False
    return True

def Forced(G):
    """Return dictionary mapping variables to forced values, or None if unsatisfiable."""
    Force = {}
    Sym = Symmetrize(G)
    Con = Condensation(Sym)
    Map = {}
    for SCC in Con:
        for v in SCC:
            Map[v] = SCC
    Reach = Reachability(Con)
    for v in Sym:
        if Reach.reachable(Map[v],Map[Not(v)]): # v implies not v?
            value = False
            if isinstance(v,SymbolicNegation):
                v = Not(v)
                value = True
            if v in Force:  # already added by negation?
                return None
            Force[v] = value
    return Force

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
