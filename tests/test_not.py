import unittest

from pads._not import Not


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
        D = {Not(x):x for x in NotNotTest.things}
        for x in NotNotTest.things:
            self.assertEqual(D[Not(x)],x)
