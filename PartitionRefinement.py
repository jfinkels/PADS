"""PartitionRefinement.py

Maintain and refine a partition of a set of items into subsets,
as used e.g. in Hopcroft's DFA minimization algorithm,
modular decomposition of graphs, etc.

D. Eppstein, November 2003.
"""

from sets import Set

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
        self._sets = [S]
        self._setids = Set([id(S)])
        self._partition = dict([(x,S) for x in S])
        
    def __get__(self,element):
        """Return the set that contains the given element."""
        return self._partition[element]
        
    def __iter__(self):
        """Loop through the sets in the partition."""
        return iter(self._sets)
        
    def __len__(self):
        """Return the number of sets in the partition."""
        return len(self._sets)

    def add(self,element,set):
        """Add a new element to the given partition subset."""
        if id(set) not in self._setids:
            raise ValueError("Set does not belong to the partition")
        if element in self._partition:
            raise ValueError("Element already belongs to the partition")
        self._partition[element] = set
        set.add(element)

    def remove(self,element):
        """Remove the given element from its partition subset."""
        set = self._partition[element]
        del self._partition[element]
        set.remove(element)

    def refine(self,S):
        """Refine each set A in the partition to the two sets
        A & S, A - S.  Return a list of pairs (A & S, A - S)
        for each changed set.  Within each pair, A & S will be
        a newly created set, while A - S will be a modified
        version of an existing set in the partition.
        """
        hit = []
        ids = {}
        S = Set(S)
        for x in S:
            if x in self._partition:
                Ax = self._partition[x]
                if id(Ax) not in ids:
                    hit.append(Ax)
                    ids[id(Ax)] = Set()
                ids[id(Ax)].add(x)
        output = []
        for A in hit:
            AS = ids[id(A)]
            if AS != A:
                self._sets.append(AS)
                self._setids.add(id(AS))
                for x in AS:
                    self._partition[x] = AS
                A -= AS
                output.append((AS,A))
        return output
