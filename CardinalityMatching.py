"""CardinalityMatching.py

Find maximum cardinality matchings in general undirected graphs.

D. Eppstein, UC Irvine, September 6, 2003.
"""

from UnionFind import UnionFind

if 'True' not in globals():
    globals()['True'] = not None
    globals()['False'] = not True

def matching(G, initialMatching = {}):
    """Find a maximum cardinality matching in a graph G.
    G is represented in modified GvR form: iter(G) lists its vertices;
    iter(G[v]) lists the neighbors of v; w in G[v] tests adjacency.
    For maximal efficiency, G and G[v] should be dictionaries, so
    that adjacency tests take constant time each.
    The output is a dictionary mapping vertices to their matches;
    unmatched vertices are omitted from the dictionary.
    
    We use Edmonds' blossom-contraction algorithm, as described e.g.
    in Galil's 1986 Computing Surveys paper.
    """

    # Copy initial matching so we can use it nondestructively
    matching = {}
    for x in initialMatching:
        matching[x] = initialMatching[x]


    # Form greedy matching to avoid some iterations of augmentation
    for v in G:
        if v not in matching:
            for w in G[v]:
                if w not in matching:
                    matching[v] = w
                    matching[w] = v
                    break

    def augment():
        """Search for a single augmenting path.
        Returns true if the matching size was increased, false otherwise.
        """
    
        # Data structures for augmenting path search:
        #
        # leader: union-find structure; the leader of a blossom is one
        # of its vertices (not necessarily topmost), and leader[v] always
        # points to the leader of the largest blossom containing v
        #
        # S: dictionary of blossoms at even levels of the structure tree.
        # Dictionary keys are names of blossoms (as returned by the union-find
        # data structure) and values are the structure tree parent of the blossom
        # (a T-node, or the top vertex if the blossom is a root of a structure tree).
        #
        # T: dictionary of vertices at odd levels of the structure tree.
        # Dictionary keys are the vertices; T[x] is a vertex with an unmatched
        # edge to x.  To find the parent in the structure tree, use leader[T[x]].
        #
        # unexplored: collection of unexplored vertices within leader of S
        #
        # base: if x was originally a T-vertex, but becomes part of a blossom,
        # base[t] will be the pair (v,w) at the base of the blossom, where v and t
        # are on the same side of the blossom and w is on the other side.

        leader = UnionFind()
        S = {}
        T = {}
        unexplored = []
        base = {}
        
        # Subroutines for augmenting path search.
        # Many of these are called only from one place, but are split out
        # as subroutines to improve modularization and readability.
        
        def blossom(v,w,a):
            """Create a new blossom from edge v-w with common ancestor a."""
            
            def findSide(v,w):
                path = [leader[v]]
                b = (v,w)   # new base for all T nodes found on the path
                while path[-1] != a:
                    tnode = S[path[-1]]
                    path.append(tnode)
                    base[tnode] = b
                    unexplored.append(tnode)
                    path.append(leader[T[tnode]])
                return path
            
            a = leader[a]   # sanity check
            path1,path2 = findSide(v,w), findSide(w,v)
            leader.union(*path1)
            leader.union(*path2)
            S[leader[a]] = S[a] # update structure tree

        topless = object()  # should be unequal to any graph vertex
        def alternatingPath(start, goal = topless):
            """Return sequence of vertices on alternating path from start to goal.
            The goal must be a T node along the path from the start to
            the root of the structure tree. If goal is omitted, we find
            an alternating path to the structure tree root.
            """
            path = []
            while 1:
                while start in T:
                    v, w = base[start]
                    vs = alternatingPath(v, start)
                    vs.reverse()
                    path += vs
                    start = w
                path.append(start)
                if start not in matching:
                    return path     # reached top of structure tree, done!
                tnode = matching[start]
                path.append(tnode)
                if tnode == goal:
                    return path     # finished recursive subpath
                start = T[tnode]
                
        def alternate(v):
            """Make v unmatched by alternating the path to the root of its structure tree."""
            path = alternatingPath(v)
            path.reverse()
            for i in range(0,len(path)-1,2):
                matching[path[i]] = path[i+1]
                matching[path[i+1]] = path[i]

        def addMatch(v, w):
            """Here with an S-S edge vw connecting vertices in different structure trees.
            Find the corresponding augmenting path and use it to augment the matching.
            """
            alternate(v)
            alternate(w)
            matching[v] = w
            matching[w] = v
            
        def ss(v,w):
            """Handle detection of an S-S edge in augmenting path search.
            Like augment(), returns true iff the matching size was increased.
            """
    
            if leader[v] == leader[w]:
                return False        # self-loop within blossom, ignore
    
            # parallel search up two branches of structure tree
            # until we find a common ancestor of v and w
            path1, head1 = {}, v
            path2, head2 = {}, w
    
            def step(path, head):
                head = leader[head]
                parent = leader[S[head]]
                if parent == head:
                    return head     # found root of structure tree
                path[head] = parent
                path[parent] = leader[T[parent]]
                return path[parent]
                
            while 1:
                head1 = step(path1, head1)
                head2 = step(path2, head2)
                
                if head1 == head2:
                    blossom(v, w, head1)
                    return False
                
                if leader[S[head1]] == head1 and leader[S[head2]] == head2:
                    addMatch(v, w)
                    return True
                
                if head1 in path2:
                    blossom(v, w, head1)
                    return False
                
                if head2 in path1:
                    blossom(v, w, head2)
                    return False    

        # Start of main augmenting path search code.

        for v in G:
            if v not in matching:
                S[v] = v
                unexplored.append(v)

        current = 0     # index into unexplored, in FIFO order so we get short paths
        while current < len(unexplored):
            v = unexplored[current]
            current += 1

            for w in G[v]:
                if leader[w] in S:  # S-S edge: blossom or augmenting path
                    if ss(v,w):
                        return True

                elif w not in T:    # previously unexplored node, add as T-node
                    T[w] = v
                    u = matching[w]
                    if leader[u] not in S:
                        S[u] = w    # and add its match as an S-node
                        unexplored.append(u)
                        
        return False    # ran out of graph without finding an augmenting path
                        
    # augment the matching until it is maximum
    while augment():
        pass

    return matching
