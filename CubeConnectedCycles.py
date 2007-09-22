"""CubeConnectedCycles.py

The cube-connected cycles network.

D. Eppstein, September 2007.
"""

def CubeConnectedCycles(n):
    G = {}
    for x in range(1<<n):
        for y in range(n):
            G[x,y] = [(x,(y+1)%n),(x,(y-1)%n),(x^(1<<y),y)]
    return G
