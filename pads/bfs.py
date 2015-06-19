"""Functions for breadth-first search in a graph.

For lexicographic breadth-first search, see :mod:`lex_bfs`.

"""


def breadth_first_levels(G, root):
    """
    Generate a sequence of bipartite directed graphs, each consisting
    of the edges from level i to level i+1 of G. Edges that connect
    vertices within the same level are not included in the output.
    The vertices in each level can be listed by iterating over each
    output graph.
    """
    visited = set()
    currentLevel = [root]
    while currentLevel:
        for v in currentLevel:
            visited.add(v)
        nextLevel = set()
        levelGraph = {v: set() for v in currentLevel}
        for v in currentLevel:
            for w in G[v]:
                if w not in visited:
                    levelGraph[v].add(w)
                    nextLevel.add(w)
        yield levelGraph
        currentLevel = nextLevel
