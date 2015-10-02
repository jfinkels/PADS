"""LongestIncreasingSubsequence.py

Find longest increasing subsequence of an input sequence.
D. Eppstein, April 2004
"""

from bisect import bisect_left


def longest_increasing_subsequence(S):
    """
    Find and return longest increasing subsequence of S.
    If multiple increasing subsequences exist, the one that ends
    with the smallest value is preferred, and if multiple
    occurrences of that value can end the sequence, then the
    earliest occurrence is preferred.
    """

    # The main data structures: head[i] is value x from S that
    # terminates a length-i subsequence, and tail[i] is either
    # None (if i=0) or the pair (head[i-1],tail[i-1]) as they
    # existed when x was processed.
    head = []
    tail = [None]

    for x in S:
        i = bisect_left(head, x)
        if i >= len(head):
            head.append(x)
            if i > 0:
                tail.append((head[i - 1], tail[i - 1]))
        elif head[i] > x:
            head[i] = x
            if i > 0:
                tail[i] = head[i - 1], tail[i - 1]

    if not head:
        return []

    output = [head[-1]]
    pair = tail[-1]
    while pair:
        x, pair = pair
        output.append(x)

    output.reverse()
    return output
