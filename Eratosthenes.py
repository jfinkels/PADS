"""Eratosthenes.py
Space-efficient version of sieve of Eratosthenes.
D. Eppstein, May 2004.

The main storage of the algorithm is a hash table D with sqrt(n)
nonempty entries for a total of O(sqrt n) space.

At any point in the algorithm, each prime p occupies a cell with key at
most 2n.  E.g. by Bertrand's postulate, there is another prime p'
between n/p and 2n/p, and p' can not yet have been included because it
is greater than sqrt n, so key pp' can not be used by any other prime;
therefore p is placed at or before key pp'<2n.  Thus, the number of
times p can have been moved from its initial placement at p^2 is < n/p.

The time for the algorithm, up to output n, is O(n) + sum_{prime p <=
sqrt(n)} O(n/p) = O(n log log n).  The algorithm also makes a recursive
call, but the recursion only generates primes up to sqrt n so its time
and space is negligible compared to the outer call.

If efficiency is a significant concern it may be better to combine
this idea with segmentation and bitvectors, as in the code by
T. Oliveira e Silva at http://www.ieeta.pt/~tos/software/prime_sieve.html

Thanks to Alex Martelli for the suggestion of keeping one prime
per entry of D, rather than a list of all prime factors of D.
"""

def primes():
    '''Yields the sequence of primes via the Sieve of Eratosthenes.'''
    yield 2                 # Only even prime.  Sieve only odd numbers.
    
    # Generate recursively the sequence of primes up to sqrt(n).
    # Each p from the sequence is used to initiate sieving at p*p.
    roots = primes()
    root = roots.next()
    square = root*root
    
    # The main sieving loop.
    # We use a hash table D such that D[n]=2p for p a prime factor of n.
    # Each prime p up to sqrt(n) appears once as a value in D, and is
    # moved to successive odd multiples of p as the sieve progresses.
    D = {}
    n = 3
    while True:
        if n >= square:     # Time to include another square?
            D[square] = root+root
            root = roots.next()
            square = root*root

        if n not in D:      # Not witnessed, must be prime.
            yield n
        else:               # Move witness p to next free multiple.
            p = D[n]
            q = n+p
            while q in D:
                q += p
            del D[n]
            D[q] = p
        n += 2              # Move on to next odd number.
