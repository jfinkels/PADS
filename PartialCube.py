"""PartialCube.py

Test whether a graph is an isometric subgraph of a hypercube.

D. Eppstein, September 2005.
"""

def distancesFrom(G,start):
    """Compute distances from start to each vertex in G via BFS."""
    D = {start:0}
    i = 0
    sequence = [start]
    while i < len(sequence):
        v = sequence[i]
        i += 1
        for w in G[v]:
            if w not in D:
                D[w] = D[v] + 1
                sequence.append(w)
    return D

def PartialCubeLabeling(G):
    """Return vertex labels with Hamming distance = graph distance."""
    label = dict([(v,0) for v in G])
    bit = 1
    
    def unlabeledEdge():
        for v in G:
            for w in G[v]:
                if label[v] == label[w]:
                    return v,w
        return None

    # make the labeling
    while True:
        e = unlabeledEdge()
        if not e:
            break
        v,w = e
        vD = distancesFrom(G,v)
        wD = distancesFrom(G,w)
        for x in G:
            if vD[x] > wD[x]:
                label[x] += bit
        bit += bit

    # check that labels across each edge differ by exactly one bit
    # (so Hamming distance <= graph distance)
    for v in G:
        for w in G[v]:
            x = label[v] ^ label[w]
            if not x:
                return None
            if x & (x-1):
                return None

    # check that Hamming distances don't decrease along BFS edges
    # (so Hamming distance >= graph distance)
    for v in G:
        D = distancesFrom(G,v)
        for u in D:
            for w in G[u]:
                if D[w] > D[u]:
                    bit = label[u] ^ label[w]
                    if bit & label[w] == bit & label[v]:
                        return None

    # here with successful labeling
    return label

def isPartialCube(G):
    return bool(PartialCubeLabeling(G))
