"""PartitionRefinement.py

Maintain and refine a partition of a set of items into subsets,
as used e.g. in Hopcroft's DFA minimization algorithm,
modular decomposition of graphs, etc.

D. Eppstein, November 2003.
"""

from sets import Set, ImmutableSet

class PartitionError(Exception): pass

class PartitionRefinement:
    """Maintain and refine a partition of a set of items into subsets.
    Space usage for a partition of n items is O(n), and each refine
    operation takes time proportional to the size of its argument.
    """

    def __init__(self,items):
        """Create a new partition refinement data structure for the given
        items.  Initially, all items belong to the same subset.
        """
        S = Set(items)
        self._sets = {id(S):S}
        self._partition = dict([(x,S) for x in S])
        
    def __getitem__(self,element):
        """Return the set that contains the given element."""
        return self._partition[element]
        
    def __iter__(self):
        """Loop through the sets in the partition."""
        return self._sets.itervalues()
        
    def __len__(self):
        """Return the number of sets in the partition."""
        return len(self._sets)

    def add(self,element,set):
        """Add a new element to the given partition subset."""
        if id(set) not in self._sets:
            raise PartitionError("Set does not belong to the partition")
        if element in self._partition:
            raise PartitionError("Element already belongs to the partition")
        set.add(element)
        self._partition[element] = set

    def remove(self,element):
        """Remove the given element from its partition subset."""
        self._partition[element].remove(element)
        del self._partition[element]

    def refine(self,S):
        """Refine each set A in the partition to the two sets
        A & S, A - S.  Return a list of pairs (A & S, A - S)
        for each changed set.  Within each pair, A & S will be
        a newly created set, while A - S will be a modified
        version of an existing set in the partition.
        """
        hit = {}
        output = []
        for x in S:
            if x in self._partition:
                Ax = self._partition[x]
                hit.setdefault(id(Ax),Set()).add(x)
        for A,AS in hit.items():
            A = self._sets[A]
            if AS != A:
                self._sets[id(AS)] = AS
                for x in AS:
                    self._partition[x] = AS
                A -= AS
                output.append((AS,A))
        return output

    def freeze(self):
        """Make all sets in S immutable."""
        for S in self._sets.values():
            I = ImmutableSet(S)
            for x in I:
                self._partition[x] = I
            self._sets[id(I)] = I
            del self._sets[id(S)]
