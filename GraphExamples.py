"""GraphExamples.py

Various examples of small standard named graphs.

D. Eppstein, September 2005.
"""

def GeneralizedPetersenGraph(n,k):
    G = {}
    for i in range(n):
        G[i,True] = (i,False),((i-1)%n,True),((i+1)%n,True)
        G[i,False] = (i,True),((i-k)%n,False),((i+k)%n,False)
    return G

PetersenGraph = GeneralizedPetersenGraph(5,2)
DesarguesGraph = GeneralizedPetersenGraph(10,3)

def GeneralizedCoxeterGraph(n,a,b):
    G = {}
    for i in range(n):
        G[i,0] = (i,1),(i,2),(i,3)
        G[i,1] = (i,0),((i+1)%n,1),((i-1)%n,1)
        G[i,2] = (i,0),((i+a)%n,2),((i-a)%n,2)
        G[i,3] = (i,0),((i+b)%n,1),((i-b)%n,1)
    return G

CoxeterGraph = GeneralizedCoxeterGraph(7,2,3)

def LeviGraph():
    G = {}
    for i in range(30):
        G[i] = (i-1)%30, (i+1)%30, (i+[7,-7,9,13,-13,-9][i%6])%30
    return G
