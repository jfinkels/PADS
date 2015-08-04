import unittest

from pads.eratosthenes import primes
from pads.eratosthenes import practical_numbers


class SieveTest(unittest.TestCase):    
    def testPrime(self):
        """Test that the first few primes are generated correctly."""
        G = primes()
        for p in [2,3,5,7,11,13,17,19,23,29,31,37]:
            self.assertEqual(p,next(G))

    def testPractical(self):
        """Test that the first few practical nos are generated correctly."""
        G = practical_numbers()
        for p in [1,2,4,6,8,12,16,18,20,24,28,30,32,36]:
            self.assertEqual(p,next(G))
