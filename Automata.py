"""Automata.py

Manipulation of and conversions between regular expressions,
deterministic finite automata, and nondeterministic finite automata.

D. Eppstein, UC Irvine, November 2003.
"""

from __future__ import generators

import sys
import unittest

from sets import Set,ImmutableSet
from PartitionRefinement import PartitionRefinement
from Sequence import Sequence

class InputError(Exception): pass

# maintain Python 2.2 compatibility
if 'True' not in globals():
    globals()['True'] = not None
    globals()['False'] = not True

class Language:
    """Object representing the language recognized by a DFA or NFA.
    Available operations are testing whether a string is in the language,
    and testing whether two languages are equal.
    """
    def __init__(self,aut):
        self._recognizer = aut
    
    def __contains__(self,inputsequence):
        return self._recognizer(inputsequence)
        
    def __eq__(self,other):
        if not isinstance(other,language):
            return None
        return self._recognizer.minimize() == other._recognizer.minimize()
        
    def __ne__(self,other):
        return not (self == other)

class Automaton:
    """Base class for DFA and NFA.  This class should not be instantiated
    on its own, but dispatches methods that are appropriate to both types
    of automaton by calling .asDFA() or .asNFA() to convert the automaton
    to the appropriate type.  All automaton instances should include the
    following instance variables and methods:
     - x.initial: initial state (for DFA) or set of states (for NFA)
     - x.alphabet: set of input symbols accepted by the automaton
     - x.transition(state,symbol): result of transition function,
       either a single state (for a DFA) or set of states (for an NFA)
     - x.isfinal(state): whether the state is an accepting state
     - x.asDFA(): return an equivalent DFA
     - x.asNFA(): return an equivalent NFA
    """
    
    def __len__(self):
        """How many states does this automaton have?"""
        return len(list(self.states()))

    def __call__(self,symbols):
        """Test whether sequence of symbols is accepted by the DFA."""
        return self.asDFA()(symbols)
    
    def states(self):
        """Generate sequence of all automaton states."""
        return self.asNFA().states()

    def pprint(self,output=sys.stdout):
        """Pretty-print this automaton to an output stream."""
        return self.asNFA().pprint(output)
    
    def minimize(self):
        """Return smallest equivalent DFA."""
        return _MinimumDFA(self.asDFA())

    def reverse(self):
        """Construct NFA for reversal of original NFA's language."""
        return _ReverseNFA(self.asNFA())

    def renumber(self,offset=0):
        """Replace complicated state objects by small integers."""
        return _RenumberNFA(self.asNFA())
        
    def RegExp(self):
        """Return equivalent regular expression."""
        return self.asNFA().RegExp()

class DFA(Automaton):
    """Base class for deterministic finite automaton.  Subclasses are
    responsible for filling out the details of the initial state, alphabet,
    and transition function.
    """
    def asDFA(self):
        return self
        
    def asNFA(self):
        return _NFAfromDFA(self)

    def __call__(self,symbols):
        """Test whether sequence of symbols is accepted by the DFA."""
        state = self.initial
        for symbol in symbols:
            if symbol not in self.alphabet:
                raise InputError("Symbol " + repr(symbol) +
                                 " not in input alphabet")
            state = self.transition(state,symbol)
        return self.isfinal(state)
        
    def __eq__(self,other):
        """Report whether these two DFAs have equivalent states."""
        if not isinstance(other,DFA) or len(self) != len(other) \
                or self.alphabet != other.alphabet:
            return False
        equivalences = {self.initial:other.initial}
        unprocessed = [self.initial]
        while unprocessed:
            x = unprocessed.pop()
            y = equivalences[x]
            for c in self.alphabet:
                xc = self.transition(x,c)
                yc = other.transition(y,c)
                if xc not in equivalences:
                    equivalences[xc] = yc
                    unprocessed.append(xc)
                elif equivalences[xc] != yc:
                    return False
        return True
        
    def __ne__(self,other):
        """Report whether these two DFAs have equivalent states."""
        return not (self == other)

class NFA(Automaton):
    """Base class for nondeterministic finite automaton.  Subclasses are
    responsible for filling out the details of the initial state, alphabet,
    and transition function.  Note that the NFAs defined here do not allow
    epsilon-transitions.  Results of self.initial and self.transition are
    assumed to be represented as ImmutableSet instances.
    """
    def asNFA(self):
        return self
        
    def asDFA(self):
        return _DFAfromNFA(self)

    def states(self):
        visited = Set()
        unvisited = Set(self.initial)
        while unvisited:
            state = iter(unvisited).next()
            yield state
            unvisited.remove(state)
            visited.add(state)
            for symbol in self.alphabet:
                unvisited |= self.transition(state,symbol) - visited

    def pprint(self,output=sys.stdout):
        """Pretty-print this NFA to an output stream."""
        for state in self.states():
            adjectives = []
            if state in self.initial:
                adjectives.append("initial")
            if self.isfinal(state):
                adjectives.append("accepting")
            if not [c for c in self.alphabet if self.transition(state,c)]:
                adjectives.append("terminal")
            if not adjectives:
                print >>output, state
            else:
                print >>output, state, "(" + ", ".join(adjectives) + ")"
            for c in self.alphabet:
                for neighbor in self.transition(state,c):
                    print >>output, "  --[" + str(c) + "]-->", neighbor
    def RegExp(self):
        """Convert to regular expression and return as a string.
        See Sipser for an explanation of this algorithm."""
        
        # create artificial initial and final states
        initial = object()
        final = object()
        states = Set([initial,final]) | Set(self.states())
        
        # 2d matrix of expressions connecting each pair of states
        expr = {}
        for x in states:
            for y in states:
                expr[x,y] = None
        for x in self.states():
            if x in self.initial:
                expr[initial,x] = ''
            if self.isfinal(x):
                expr[x,final] = ''
            expr[x,x] = ''
        for x in self.states():
            for c in self.alphabet:
                for y in self.transition(x,c):
                    if expr[x,y]:
                        expr[x,y] += '+' + str(c)
                    else:
                        expr[x,y] = str(c)

        # eliminate states one at a time
        for s in self.states():
            states.remove(s)
            for x in states:
                for y in states:
                    if expr[x,s] is not None and expr[s,y] is not None:
                        xsy = []
                        if expr[x,s]:
                            xsy += self._parenthesize(expr[x,s])
                        if expr[s,s]:
                            xsy += self._parenthesize(expr[s,s],True) + ['*']
                        if expr[s,y]:
                            xsy += self._parenthesize(expr[s,y])
                        if expr[x,y] is not None:
                            xsy += ['+',expr[x,y] or '()']
                        expr[x,y] = ''.join(xsy)
        return expr[initial,final]

    def _parenthesize(self,expr,starring=False):
        """Return list of strings with or without parens for use in RegExp.
        This is only for the purpose of simplifying the expressions returned,
        by omitting parentheses or other expression features when unnecessary;
        it would always be correct simply to return ['(',expr,')'].
        """
        if len(expr) == 1 or (not starring and '+' not in expr):
            return [expr]
        elif starring and expr.endswith('+()'):
            return ['(',expr[:-3],')']  # +epsilon redundant when starring
        else:
            return ['(',expr,')']

class _DFAfromNFA(DFA):
    """Conversion of NFA to DFA.  We create a DFA state for each set
    of NFA states. A DFA state is final if it contains at least one
    final NFA set, and the transition function for a DFA state is the
    union of the transition functions of the NFA states it contains.
    """
    def __init__(self,N):
        self.initial = N.initial
        self.alphabet = N.alphabet
        self.NFA = N
    
    def transition(self,stateset,symbol):
        output = Set()
        for state in stateset:
            output |= self.NFA.transition(state,symbol)
        return ImmutableSet(output)

    def isfinal(self,stateset):
        for state in stateset:
            if self.NFA.isfinal(state):
                return True
        return False

class _NFAfromDFA(NFA):
    """Conversion of DFA to NFA.  We convert the initial state and the
    results of each transition function into single-element sets.
    """
    def __init__(self,D):
        self.initial = ImmutableSet([D.initial])
        self.alphabet = D.alphabet
        self.DFA = D
    
    def transition(self,state,symbol):
        return ImmutableSet([self.DFA.transition(state,symbol)])
    
    def isfinal(self,state):
        return self.DFA.isfinal(state)

Empty = ImmutableSet()

class RegExp(NFA):
    """Convert regular expression to NFA."""

    def __init__(self,expr):
        self.expr = expr
        self.pos = 0
        self.nstates = 0
        self.expect = {}
        self.successor = {}
        self.alphabet = Set()
        self.initial,penultimate,epsilon = self.expression()
        final = self.newstate(None)
        for state in penultimate:
            self.successor[state].add(final)
        self.final = ImmutableSet([final])
        if epsilon:
            self.final = self.final | self.initial

    def transition(self,state,c):
        """Implement NFA transition function."""
        if c != self.expect[state]:
            return Empty
        else:
            return self.successor[state]

    def isfinal(self,state):
        """Implement NFA acceptance test."""
        return state in self.final

    # Recursive-descent parser for regular expressions.
    # Each function uses self.pos as a pointer into self.expr,
    # updates self.expect and self.successor,
    # and returns a tuple (initial,penultimate,epsilon), where
    #   initial = the initial states of the subexpression
    #   penultimate = states one step away from an accepting state
    #   epsilon = true if the subexpression accepts the empty string
    
    def epsilon(self):
        """Parse an empty string and return an empty automaton."""
        return Empty,Empty,True

    def newstate(self,expect):
        """Allocate a new state in which we expect to see the given letter."""
        state = self.nstates
        self.successor[state] = Set()
        self.expect[state] = expect
        self.nstates += 1
        return state

    def base(self):
        """Parse a subexpression that can be starred: single letter or group."""
        if self.pos == len(self.expr) or self.expr[self.pos] == ')':
            return self.epsilon()
        if self.expr[self.pos] == '(':
            self.pos += 1
            ret = self.expression()
            if self.pos == len(self.expr) or self.expr[self.pos] != ')':
                raise RegExpError("Close paren expected at char " + str(self.pos))
            self.pos += 1
            return ret
        if self.expr[self.pos] == '\\':
            self.pos += 1
            if self.pos == len(self.expr):
                raise RegExpError("Character expected after backslash")
        self.alphabet.add(self.expr[self.pos])
        state = self.newstate(self.expr[self.pos])
        self.pos += 1
        state = ImmutableSet([state])
        return state,state,False

    def factor(self):
        """Parse a catenable expression: base or starred base."""
        initial,penultimate,epsilon = self.base()
        while self.pos < len(self.expr) and self.expr[self.pos] == '*':
            self.pos += 1
            for state in penultimate:
                self.successor[state] |= initial
            epsilon = True
        return initial,penultimate,epsilon
        
    def term(self):
        """Parse a summable expression: factor or concatenation."""
        initial,penultimate,epsilon = self.factor()
        while self.pos < len(self.expr) and self.expr[self.pos] not in ')+':
            Fi,Fp,Fe = self.factor()
            for state in penultimate:
                self.successor[state] |= Fi
            if epsilon:
                initial = initial | Fi
            if Fe:
                penultimate = penultimate | Fp
            else:
                penultimate = Fp
            epsilon = epsilon and Fe
        return initial,penultimate,epsilon

    def expression(self):
        """Parse a whole regular expression or grouped subexpression."""
        initial,penultimate,epsilon = self.term()
        while self.pos < len(self.expr) and self.expr[self.pos] == '+':
            self.pos += 1
            Ti,Tp,Te = self.term()
            initial = initial | Ti
            penultimate = penultimate | Tp
            epsilon = epsilon or Te
        return initial,penultimate,epsilon

class LookupNFA(NFA):
    """Construct NFA with precomputed lookup table of transitions."""
    def __init__(self,alphabet,initial,ttable,final):
        self.alphabet = alphabet
        self.initial = ImmutableSet(initial)
        self.ttable = ttable
        self.final = ImmutableSet(final)
        
    def transition(self,state,symbol):
        return ImmutableSet(self.ttable[state,symbol])
        
    def isfinal(self,state):
        return state in self.final

def _RenumberNFA(N,offset=0):
    """Replace NFA state objects with small integers."""
    replacements = {}
    for x in N.states():
        replacements[x] = offset
        offset += 1
    initial = [replacements[x] for x in N.initial]
    ttable = {}
    for state in N.states():
        for symbol in N.alphabet:
            ttable[replacements[state],symbol] = [replacements[x]
                for x in N.transition(state,symbol)]
    final = [replacements[x] for x in N.states() if N.isfinal(x)]
    return LookupNFA(N.alphabet,initial,ttable,final)

def _ReverseNFA(N):
    """Construct NFA for reversal of original NFA's language."""
    initial = [s for s in N.states() if N.isfinal(s)]
    ttable = dict([((s,c),[]) for s in N.states() for c in N.alphabet])
    for s in N.states():
        for c in N.alphabet:
            for t in N.transition(s,c):
                ttable[t,c].append(s)
    return LookupNFA(N.alphabet,initial,ttable,N.initial)

class _MinimumDFA(DFA):
    """Construct equivalent DFA with minimum number of states,
    using Hopcroft's O(ns log n) partition-refinement algorithm.
    """
    def __init__(self,D):
        # refine partition of states by reversed neighborhoods
        N = D.reverse()
        P = PartitionRefinement(D.states())
        P.refine([s for s in D.states() if D.isfinal(s)])
        unrefined = Sequence(P,key=id)
        while unrefined:
            part = iter(unrefined).next()
            unrefined.remove(part)
            for symbol in D.alphabet:
                neighbors = Set()
                for state in part:
                    neighbors |= N.transition(state,symbol)
                for new,old in P.refine(neighbors):
                    if old in unrefined or len(new) < len(old):
                        unrefined.append(new)
                    else:
                        unrefined.append(old)
        
        # convert partition to DFA
        P.freeze()
        self.partition = P
        self.initial = P[D.initial]
        self.alphabet = D.alphabet
        self.DFA = D
        
    def transition(self,state,symbol):
        rep = iter(state).next()
        return self.partition[self.DFA.transition(rep,symbol)]
        
    def isfinal(self,state):
        rep = iter(state).next()
        return self.DFA.isfinal(rep)

# If called as standalone routine, run some unit tests

class RegExpTest(unittest.TestCase):
    # dictionary of regexp:([strings in L],[strings not in L])
    RegExps = {
        "0": (["0"],["","00"]),
        "(10+0)*": (["","0","010"],["1"]),
        "(0+1)*1(0+1)(0+1)": (["000100"],["0011"]),
    }

    def testMembership(self):
        for R in self.RegExps:
            L = Language(RegExp(R))
            for S in self.RegExps[R][0]:
                self.assert_(S in L)
            for S in self.RegExps[R][1]:
                self.assert_(S not in L)

    def testEquivalent(self):
        for R in self.RegExps:
            N1 = RegExp(R)
            N2 = RegExp(N1.RegExp())
            self.assertEqual(N1.minimize(),N2.minimize())
    
    def testInequivalent(self):
        automata = [RegExp(R).minimize() for R in self.RegExps]
        for i in range(len(automata)):
            for j in range(i):
                self.assertNotEqual(automata[i],automata[j])
                
if __name__ == "__main__":
    unittest.main()   