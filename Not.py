"""Not.py

Symbolic negation operator.

D. Eppstein, April 2009.
"""

import unittest

class DoubleNegationError(Exception): pass

class SymbolicNegation:
    def __init__(self,x):
        if isinstance(x,SymbolicNegation):
            raise DoubleNegationError("Use Not(x) rather than instantiating SymbolicNegation directly")
        self.negation = x

    def negate(self):
        return self.negation
        
    def __repr__(self):
        return "Not(" + repr(self.negation) + ")"

    def __eq__(self,other):
        return isinstance(other,SymbolicNegation) and self.negation == other.negation

    def __hash__(self):
        return -hash(self.negation)

def Not(x):
    if isinstance(x,SymbolicNegation):
        return x.negate()
    else:
        return SymbolicNegation(x)

class NotNotTest(unittest.TestCase):
    things = [None,3,"ABC",Not(27)]
    def testNot(self):
        for x in NotNotTest.things:
            self.assertEqual(Not(Not(x)),x)
    def testEq(self):
        for x in NotNotTest.things:
            for y in NotNotTest.things:
                self.assertEqual(Not(x)==Not(y),x==y)
    def testHash(self):
        D = dict([(Not(x),x) for x in NotNotTest.things])
        for x in NotNotTest.things:
            self.assertEqual(D[Not(x)],x)

if __name__ == "__main__":
    unittest.main()   
