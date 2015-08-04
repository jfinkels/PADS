import unittest

from pads.cubic_ham import hamiltonian_cycles
from pads.cubic_ham import arbitrary_item


class CubicHamTest(unittest.TestCase):
    def check(self,G,N):
        """Make sure G has N Hamiltonian cycles."""
        count = 0
        for C in hamiltonian_cycles(G):
            # Count the cycle.
            count += 1

            # Check that it's a degree-two undirected subgraph.
            for v in C:
                self.assertEqual(len(C[v]),2)
                for w in C[v]:
                    assert v in G and w in G[v] and v in C[w]

            # Check that it connects all vertices.
            nreached = 0
            x = arbitrary_item(G)
            a,b = x,x
            while True:
                nreached += 1
                a,b = b,[z for z in C[b] if z != a][0]
                if b == x:
                    break
            self.assertEqual(nreached,len(G))

        # Did we find enough cycles?
        self.assertEqual(count,N)

    def testCube(self):
        """Cube has six Hamiltonian cycles."""
        cube = {i:(i^1,i^2,i^4) for i in range(8)}
        self.check(cube,6)

    def twistedLadder(self,n):
        """Connect opposite vertices on an even length cycle."""
        return {i:((i+1)%n,(i-1)%n,(i+n//2)%n) for i in range(n)}

    def testEvenTwistedLadders(self):
        """twistedLadder(4n) has 2n+1 Hamiltonian cycles."""
        for n in range(4,50,4):
            self.check(self.twistedLadder(n),n//2+1)

    def testOddTwistedLadders(self):
        """twistedLadder(4n+2) has 2n+4 Hamiltonian cycles."""
        for n in range(6,50,4):
            self.check(self.twistedLadder(n),n//2+3)

    def truncate(self,G):
        """Replace each vertex of G by a triangle and return the result."""
        return {(v,w):{(v,u) for u in G[v] if u != w} | {(w,v)}
                for v in G for w in G[v]}

    def testSierpinski(self):
        """
        Sierpinski triangle like graphs formed by repeated truncation
        of K_4 should all have exactly three Hamiltonian cycles.
        """
        G = self.twistedLadder(4)   # Complete graph on four vertices
        for i in range(3):
            G = self.truncate(G)
            self.check(G,3)
