"""Lyndon.py
Algorithms on strings and sequences based on Lyndon words.
David Eppstein, October 2011."""

import unittest
from Eratosthenes import MoebiusFunction

def LengthLimitedLyndonWords(s,n):
    """Generate nonempty Lyndon words of length <= n over an s-symbol alphabet.
    The words are generated in lexicographic order, using an algorithm from
    J.-P. Duval, Theor. Comput. Sci. 1988, doi:10.1016/0304-3975(88)90113-2.
    As shown by Berstel and Pocchiola, it takes constant average time
    per generated word."""
    w = [-1]                            # set up for first increment
    while w:
        w[-1] += 1                      # increment the last non-z symbol
        yield w
        m = len(w)
        while len(w) < n:               # repeat word to fill exactly n syms
            w.append(w[-m])
        while w and w[-1] == s - 1:     # delete trailing z's
            w.pop()

def LyndonWordsWithLength(s,n):
    """Generate Lyndon words of length exactly n over an s-symbol alphabet.
    Since nearly half of the outputs of LengthLimitedLyndonWords(s,n)
    have the desired length, it again takes constant average time per word."""
    if n == 0:
        yield []    # the empty word is a special case not handled by main alg
    for w in LengthLimitedLyndonWords(s,n):
        if len(w) == n:
            yield w

def LyndonWords(s):
    """Generate all Lyndon words over an s-symbol alphabet.
    The generation order is by length, then lexicographic within each length."""
    n = 0
    while True:
        for w in LyndonWordsWithLength(s,n):
            yield w
        n += 1

def DeBruijnSequence(s,n):
    """Generate a De Bruijn sequence for words of length n over s symbols
    by concatenating together in lexicographic order the Lyndon words
    whose lengths divide n. The output length will be s^n.
    Because nearly half of the generated sequences will have length
    exactly n, the algorithm will take O(s^n/n) steps, and the bulk
    of the time will be spent in sequence concatenation."""
    
    output = []
    for w in LengthLimitedLyndonWords(s,n):
        if n % len(w) == 0:
            output += w
    return output

def CountLyndonWords(s,n):
    """The number of length-n Lyndon words over s symbols."""
    if n == 0:
        return 1
    total = 0
    for i in range(1,n+1):
        if n%i == 0:
            total += MoebiusFunction(n/i) * s**i
    return total//n

# If run standalone, perform unit tests
class LyndonTest(unittest.TestCase):    
    def testCount(self):
        """Test that we count Lyndon words correctly."""
        for s in range(2,6):
            for n in range(1,5):
                self.assertEqual(CountLyndonWords(s,n),
                    len(list(LyndonWordsWithLength(s,n))))

    def testOrder(self):
        """Test that we generate Lyndon words in lexicographic order."""
        for s in range(2,6):
            for n in range(1,5):
                prev = None
                for x in LengthLimitedLyndonWords(s,n):
                    self.assert_(prev < x)
                    prev = list(x)

    def testSubsequence(self):
        """Test that words of length n-1 are a subsequence of length n."""
        for s in range(2,6):
            for n in range(2,5):
                smaller = LengthLimitedLyndonWords(s,n-1)
                for x in LengthLimitedLyndonWords(s,n):
                    if len(x) < n:
                        self.assertEqual(x,smaller.next())

    def testDeBruijn(self):
        """Test that the De Bruijn sequence is correct."""
        for s in range(2,6):
            for n in range(2,5):
                db = DeBruijnSequence(s,n)
                self.assertEqual(len(db), s**n)
                db = db + db    # duplicate so we can wrap easier
                subs = set(tuple(db[i:i+n]) for i in range(s**n))
                self.assertEqual(len(subs), s**n)

if __name__ == "__main__":
    unittest.main()
