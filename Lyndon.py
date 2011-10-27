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

def LyndonWords(s):
    """Generate all Lyndon words over an s-symbol alphabet.
    The generation order is by length, then lexicographic within each length.
    Since nearly half of the outputs of LengthLimitedLyndonWords(s,n)
    have the desired length, it again takes constant average time per word."""
    yield []    # the empty word is a special case not handled by main alg
    n = 1
    while True:
        for w in LengthLimitedLyndonWords(s,n):
            if len(w) == n:
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
