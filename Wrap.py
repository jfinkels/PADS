"""Wrap.py

Break paragraphs into lines, attempting to avoid short lines.

We use the dynamic programming idea of Knuth-Plass to find the
optimal set of breaks according to a penalty function that
penalizes short lines quadratically; this can be done in linear
time via the OnlineConcaveMinima algorithm in SMAWK.py.

D. Eppstein, August 2005.
"""

from SMAWK import OnlineConcaveMinima

def wrap(text,                  # string or unicode to be wrapped
         longlast = False,      # True if last line should be as long as others
         target = 72,           # maximum length of a wrapped line
         measure = len,         # how to measure the length of a word
         overpenalty = 100000,  # penalize long lines by overpen*(len-target)
         nlinepenalty = 100000, # penalize more lines than optimal
         hyphenpenalty = 100):   # penalize breaking hyphenated words
    """Wrap the given text, returning a sequence of lines."""

    # Make sequence of tuples (word, space if no break, cum.measure).
    words = []
    total = 0
    space = measure(' ')
    for hyphenword in text.split():
        if total:
            total += space
        parts = hyphenword.split('-')
        for word in parts[:-1]:
            word += '-'
            total += measure(word)
            words.append((word,False,total))
        word = parts[-1]
        total += measure(word)
        words.append((word,True,total))

    # Define penalty function for breaking on line words[i:j]
    # Below this definition we will set up cost[i] to be the
    # total penalty of all lines up to a break prior to word i.
    def penalty(i,j):
        if j > len(words): return -i    # concave flag for out of bounds
        total = cost.value(i) + nlinepenalty
        prevmeasure = i and words[i-1][2]
        linemeasure = words[j-1][2] - prevmeasure
        if linemeasure > target:
            total += overpenalty * (linemeasure - target)
        elif j < len(words) or longlast:
            total += (target - linemeasure)**2
        if not words[j-1][1]:
            total += hyphenpenalty
        return total

    # Apply concave minima algorithm and backtrack to form lines
    cost = OnlineConcaveMinima(penalty,0)
    pos = len(words)
    lines = []
    while pos:
        breakpoint = cost.index(pos)
        line = []
        for i in range(breakpoint,pos):
            line.append(words[i][0])
            if i < pos-1 and words[i][1]:
                line.append(' ')
        lines.append(''.join(line))
        pos = breakpoint
    lines.reverse()
    return lines
