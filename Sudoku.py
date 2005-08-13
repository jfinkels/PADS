"""Sudoku.py

PADS-based command-line application for generating and solving Sudoku puzzles.
These puzzles are given as a 9x9 grid of cells, some of which are filled with
digits in the range 1-9.  The task is to fill the remaining cells in such a
way that each row of the grid, each column of the grid, and each of nine 3x3
squares into which the grid is partitioned, all have one copy of each of the
nine digits.

A proper Sudoku puzzle must have a unique solution, and it should be possible
to reach that solution by a sequence of logical deductions without trial and
error.  To the extent possible, we strive to keep the same ethic in our
automated solver, by mimicking human rule-based reasoning, rather than
resorting to brute force backtracking search.

D. Eppstein, July 2005.
"""

import random
import sys
from optparse import OptionParser
from BipartiteMatching import imperfections
from StrongConnectivity import StronglyConnectedComponents
from Repetitivity import NonrepetitiveGraph

try:
    set
except NameError:
    from sets import Set as set

class BadSudoku(Exception): pass
    # raised when we discover that a puzzle has no solutions

# ======================================================================
#   Bitmaps and patterns
# ======================================================================

digits = range(1,10)

class group:
    def __init__(self, i, j, x, y, name):
        mask = 0
        h,k = [q for q in range(4) if q != i and q != j]
        for w in range(3):
            for z in range(3):
                mask |= 1L << (x*3**i + y*3**j + w*3**h + z*3**k)
        self.mask = mask
        self.pos = [None]*9
        self.name = "%s %d" % (name,x+3*y+1)

cols = [group(0,1,x,y,"col") for x in range(3) for y in range(3)]
rows = [group(2,3,x,y,"row") for x in range(3) for y in range(3)]
sqrs = [group(1,3,x,y,"sqr") for x in range(3) for y in range(3)]
groups = rows+cols+sqrs

neighbors = [0]*81
for i in range(81):
    b = 1L<<i
    for g in groups:
        if g.mask & b:
            neighbors[i] |= (g.mask &~ b)

unmask = {}
for i in range(81):
    unmask[1L<<i] = i

alignments = {}
for s in sqrs:
    for g in rows+cols:
        m = s.mask&g.mask
        if m:
            alignments[m] = (s,g)
            b1 = m &~ (m-1)
            m &=~ b1
            b2 = m &~ (m-1)
            b3 = m &~ b2
            alignments[b1|b2]=alignments[b1|b3]=alignments[b2|b3]=(s,g)   

triads = []
for square in sqrs:
    for group in rows+cols:
        triads.append((square.mask & group.mask,square,group))

# ======================================================================
#   State for puzzle solver
# ======================================================================

class Sudoku:
    """
    Data structure for storing and manipulating Sudoku puzzles.
    The actual rules for solving the puzzles are implemented
    separately from this class.
    """

    def __init__(self,initial_placements = None):
        """
        Initialize a new Sudoku grid.
        
        If an argument is given, it should either be a sequence of 81
        digits 0-9 (0 meaning a not-yet-filled cell), or a sequence
        of (digit,cell) pairs.
        
        The main state we use for the solver is an array contents[]
        of 81 cells containing digits 0-9 (0 for an unfilled cell)
        and an array locations[] indexed by the digits 1-9, containing
        bitmasks of the cells still available to each digit.
        
        We also store additional fields:

        - progress is a boolean, set whenever one of our methods
          changes the state of the puzzle, and used by step() to tell
          whether one of its rules fired.
          
        - rules_used is a set of the rule names that have made progress.
        
        - pairs is a dictionary mapping bitmasks of pairs of cells to
          lists of digits that must be located in that pair, as set up
          by the pair rule and used by other later rules.
          
        - bilocation is a NonrepetitiveGraph representing paths and
          cycles among bilocated digits, as constructed by the bilocal
          rule and used by the repeat and conflict rules.
        
        - bivalues is a NonrepetitiveGraph representing paths and
          cycles among bivalued cells, as constructed by the bivalue
          rule and used by the repeat and conflict rules.
          
        - otherbv maps pairs (cell,digit) in the bivalue graph to the
          other digit available at the same cell
        
        - verbose is used to enable or disable solution step logging.
        """
        self.contents = [0]*81
        self.locations = [None]+[(1L<<81)-1]*9
        self.rules_used = set()
        self.progress = False
        self.pairs = None
        self.bilocation = None
        self.verbose = False

        if initial_placements:
            cell = 0
            for item in initial_placements:
                try:
                    digit = int(item)
                except TypeError:
                    digit,cell = item
                if digit:
                    self.place(digit,cell)
                cell += 1
        
    def __iter__(self):
        """
        If we are asked to loop over the items in a grid
        (for instance, if we pass one Sudoku instance as the argument
        to the initialization of another one) we simply list the
        known cell contents of the grid.
        """
        return iter(self.contents)
    
    def mark_progress(self):
        """Set progress True and clear fields that depended on old state."""
        self.progress = True
        self.pairs = None

    def place(self,digit,cell):
        """Change the puzzle by filling the given cell with the given digit."""
        if digit != int(digit) or not 1 <= digit <= 9:
            raise ValueError("place(%d,%d): digit out of range" % (digit,cell))
        if self.contents[cell] == digit:
            return
        if self.contents[cell]:
            raise BadSudoku("place(%d,%d): cell already contains %d" %
                            (digit,cell,self.contents[cell]))
        if (1L<<cell) & self.locations[digit] == 0:
            raise BadSudoku("place(%d,%d): location not available" %
                            (digit+1,cell))
        self.contents[cell] = digit
        bit = 1L << cell
        for d in digits:
            if d != digit:
                self.unplace(d,bit,False)
            else:
                self.unplace(d,neighbors[cell],False)
        self.mark_progress()
        if self.verbose:
            print >>sys.stderr,"Placing digit",digit,"in cell",cell

    def unplace(self,digit,mask,log=True):
        """
        Eliminate the masked positions as possible locations for digit.
        The log argument should be true for external callers, but false
        when called by Sudoku.place; it is used to disable verbose output
        that would be redundant to the output from place.
        """
        if digit != int(digit) or not 1 <= digit <= 9:
            raise ValueError("unplace(%d): digit out of range" % digit)
        if self.locations[digit] & mask:
            if log and self.verbose:
                unbits = self.locations[digit] & mask
                unmarked = []
                while unbits:
                    bit = unbits &~ (unbits - 1)
                    unmarked.append(unmask[bit])
                    unbits &=~ bit
                print >>sys.stderr,"Preventing digit",digit,"from",
                if len(unmarked) == 1:
                    print >>sys.stderr,"cell",unmarked[0]
                else:
                    print >>sys.stderr,"cells",unmarked
            self.locations[digit] &=~ mask
            self.mark_progress()

    def choices(self,cell):
        """Which digits are still available to be placed in the cell?"""
        bit = 1L<<cell
        return [d for d in digits if self.locations[d] & bit]

    def complete(self):
        """True if all cells have been filled in."""
        return 0 not in self.contents

# ======================================================================
#   Rules for puzzle solver
# ======================================================================

def locate(grid):
    """
    Place digits that can only go in one cell of their group.
    If a digit x has only one remaining cell that it can be placed in,
    within some row, column, or square, then we place it in that cell.
    Any potential positions of x incompatible with that cell (because
    they lie in the same row, column, or square) are removed from
    future consideration.
    """
    for d in digits:
        for g in groups:
            dglocs = grid.locations[d] & g.mask
            if dglocs & (dglocs-1) == 0:
                if dglocs == 0:
                    raise BadSudoku("No place for %d in %s" %(d,g.name))
                grid.place(d,unmask[dglocs])

def eliminate(grid):
    """
    Fill cells that can only contain one possible digit.
    If a cell has only one digit x that can be placed in it, we place
    x in that cell.  Incompatible positions for x are removed from
    future consideration.
    """
    for cell in range(81):
        if not grid.contents[cell]:
            allowed = grid.choices(cell)
            if len(allowed) == 0:
                raise BadSudoku("No digit for cell %d" % cell)
            if len(allowed) == 1:
                grid.place(allowed[0],cell)

def align(grid):
    """
    Eliminate positions that leave no choices for another group.
    If the cells of a square that can contain a digit x all lie
    in a single row or column, we eliminate positions for x that
    are outside the square but inside that row or column.  Similarly,
    if the cells that can contain x within a row or column all lie
    in a single square, we eliminate positions that are inside that
    square but outside the row or column.
    """
    for d in digits:
        for g in groups:
            a = grid.locations[d] & g.mask
            if a in alignments:
                s = [x for x in alignments[a] if x != g][0]
                grid.unplace(d, s.mask &~ a)

def pair(grid):
    """
    Eliminate positions that leave no choices for two other digits.
    If two digits x and y each share the same two cells as the only
    locations they may be placed within some row, column, or square,
    then all other digits must avoid those two cells.
    """
    grid.pairs = pairs = {}
    for d in digits:
        for g in groups:
            dglocs = grid.locations[d] & g.mask
            fewerbits = dglocs & (dglocs - 1)
            if fewerbits & (fewerbits - 1) == 0:
                if d not in pairs.setdefault(dglocs,[d]):
                    pairs[dglocs].append(d)
                    for e in digits:
                        if e not in pairs[dglocs]:
                            grid.unplace(e, dglocs)

def triad(grid):
    """
    Find forced triples of digits within triples of cells.
    If some three cells, formed by intersecting a row or column
    with a square, have three digits whose only remaining positions
    within that row, column, or square are among those three cells,
    we prevent all other digits from being placed there.  We also
    remove positions for those three forced digits outside the
    triple but within the row, column, or square containing it.
    """
    for mask,sqr,grp in triads:
        forces = [d for d in digits
                  if (grid.locations[d]&sqr.mask == grid.locations[d]&mask)
                  or (grid.locations[d]&grp.mask == grid.locations[d]&mask)]
        if len(forces) == 3:
            outside = (sqr.mask | grp.mask) &~ mask
            for d in digits:
                grid.unplace(d, d in forces and outside or mask)

def digit(grid):
    """
    Remove incompatible positions of a single digit.
    If the placement of digit x in cell y can not be extended to a
    placement of nine copies of x covering each row and column of the
    grid exactly once, we eliminate cell y from consideration as
    a placement for x.
    """
    for d in digits:
        graph = {}
        locs = grid.locations[d]
        for r in range(9):
            graph[r] = [c for c in range(9)
                        if rows[r].mask & cols[c].mask & locs]
        imp = imperfections(graph)
        mask = 0
        for r in imp:
            for c in imp[r]:
                mask |= rows[r].mask & cols[c].mask
        grid.unplace(d,mask)

def subproblem(grid):
    """
    Remove incompatible positions within a single row, column, or square.
    If the placement of a digit x in cell y within a single row, column,
    or square can not be extended to a complete solution of that row, column,
    or square, then we eliminate that placement from consideration.
    """
    for g in groups:
        graph = {}
        for d in digits:
            graph[d] = []
            locs = grid.locations[d] & g.mask
            while locs:
                bit = locs &~ (locs-1)
                graph[d].append(bit)
                locs &=~ bit
        imp = imperfections(graph)
        for d in imp:
            mask = 0
            for bit in imp[d]:
                mask |= bit
            grid.unplace(d,mask)

def remotepair(grid):
    """
    Find rectangles from cells that can only contain the same two digits.
    If digits x and y are the only two digits that can occur in a sequence
    of an even number (four or more) of cells, and each two consecutive
    cells in the sequence belong to the same row, column, or square,
    then we determine the rectangle having the two endpoints of the sequence
    as corners, and eliminate x and y as possible values for the other
    two corners of the rectangle.
    """
    bivalued = {}
    for cell in range(81):
        ch = grid.choices(cell)
        if len(ch) == 2:
            bivalued.setdefault(tuple(ch),[]).append(cell)
    for pair in bivalued:
        while len(bivalued[pair]) >= 4:
            x,y = pair
            mask = (1L<<x)|(1L<<y)
            cell = bivalued[pair].pop()
            bipartition = {cell:True}
            unexplored = [cell]
            while unexplored:
                cell = unexplored.pop()
                for neighbor in bivalued[pair]:
                    if (1L<<neighbor) & neighbors[cell]:
                        bipartition[neighbor] = not bipartition[cell]
                        unexplored.append(neighbor)
                bivalued[pair] = [c for c in bivalued[pair]
                                  if c not in bipartition]
            for cell in bipartition:
                for other in bipartition:
                    if bipartition[cell] != bipartition[other] and \
                            not ((1L<<other) & neighbors[cell]):
                        corners = (1L<<((cell//9)*9 + other%9)) | \
                                  (1L<<((other//9)*9 + cell%9))
                        grid.unplace(x,corners)                    
                        grid.unplace(y,corners)                    

def bilocal(grid):
    """
    Look for nonrepetitive cycles among bilocated digits.
    Despite the sesquipedalian summary line above, this is a form of
    analysis that is easy to perform by hand: draw a graph connecting
    two cells whenever some digit's location within a row, column,
    or square is forced to lie only in those two cells.  We then
    search for cycles in the graph in which each two adjacent edges
    in the cycle have different labels. In any such cycle, each cell
    can only contain the digits labeling the two edges incident to it.
    """
    if not grid.pairs:
        return  # can only run after pair rule finds edges

    # Make labeled graph of pairs
    graph = dict([(i,{}) for i in range(81)])
    for pair in grid.pairs:
        digs = grid.pairs[pair]
        bit = pair &~ (pair-1)
        pair &=~ bit
        if pair:
            v = unmask[bit]
            w = unmask[pair]
            graph[v][w] = graph[w][v] = digs
    
    # Apply repetitivity analysis to collect cyclic labels at each cell
    grid.bilocation = nrg = NonrepetitiveGraph(graph)
    forced = [set() for i in range(81)]
    for v,w,L in nrg.cyclic():
        forced[v].add(L)
        forced[w].add(L)

    # Carry out forces indicated by our analysis
    for cell in range(81):
        if len(forced[cell]) > 2:
            raise BadSudoku(
                "triple threat in bilocal analysis: cell %s, digits %s" %
                (cell, list(forced[cell])))
        if len(forced[cell]) == 2:
            mask = 1L<<cell
            for d in digits:
                if d not in forced[cell]:
                    grid.unplace(d,mask)

def bivalue(grid):
    """
    Look for nonrepetitive cycles among bivalued cells.
    We draw a graph connecting two cells whenever both can only
    contain two digits, one of those digits is the same for both
    cells, and both cells belong to the same row, column, or square.
    Edges are labeled by the digit(s) the two cells share.
    If any edge of this graph is contained in a cycle with no two
    consecutive edges having equal labels, then the digit labeling
    that edge must be placed on one of its two endpoints, and can
    not be placed in any other cell of the row, column, or square
    containing the edge.
    """
    
    # Find and make bitmask per digit of bivalued cells
    graph = {}
    grid.otherbv = otherbv = {}
    tvmask = [0]*10
    for c in range(81):
        ch = grid.choices(c)
        if len(ch) == 2:
            graph[c] = {}
            tvmask[ch[0]] |= 1L<<c
            tvmask[ch[1]] |= 1L<<c
            otherbv[c,ch[0]] = ch[1]
            otherbv[c,ch[1]] = ch[0]
    edgegroup = {}
    
    # Form edges and map back to their groups
    for g in groups:
        for d in digits:
            mask = tvmask[d] & g.mask
            dgcells = []
            while mask:
                bit = mask &~ (mask - 1)
                dgcells.append(unmask[bit])
                mask &=~ bit
            for v in dgcells:
                for w in dgcells:
                    if v != w:
                        edgegroup.setdefault((v,w),[]).append(g)
                        graph[v].setdefault(w,set()).add(d)

    # Apply repetitivity analysis to collect cyclic labels at each cell
    # and eliminate that label from other cells of the same group
    grid.bivalues = nrg = NonrepetitiveGraph(graph)
    for v,w,digit in nrg.cyclic():
        mask = 0
        for g in edgegroup[v,w]:
            mask |= g.mask
        mask &=~ (1L << v)
        mask &=~ (1L << w)
        grid.unplace(digit,mask)

def repeat(grid):
    """
    Look for cycles of bilocated or bivalued vertices with one repetition.
    We use the same graphs described for the bilocal and bivalue rules;
    if there exists a cycle in which some two adjacent edges are labeled
    by the same digit, and all other adjacent pairs of cycle edges have
    differing digits, then the repeated digit must be placed at the cell
    where the two same-labeled edges meet (in the case of the bilocal graph)
    or can be eliminated from that cell (in the case of the bivalue graph).
    """
    if not grid.bilocation or not grid.bivalues:
        return
    for cell in range(81):
        if not grid.contents[cell]:
            for d in grid.choices(cell):
                if (cell,d) in grid.bilocation.reachable(cell,d):
                    grid.place(d,cell)
                elif (cell,d) in grid.bivalues.reachable(cell,d):
                    grid.unplace(d,1L<<cell)

def conflict(grid):
    """
    Look for conflicting paths of bilocated or bivalued cells.
    In the same graph used by the bilocal and repeat rules, if there exist
    two paths that start with the same cell and digit, and that end with
    equal digits in different cells of the same row, column, or square,
    then the start cell must contain the starting digit for otherwise
    it would cause the end cells to conflict with each other.
    One or both paths can instead be in the bivalue graph, starting and
    ending with the other digit than the one for the bilocal path.
    """
    if not grid.bilocation or not grid.bivalues:
        return
    for cell in range(81):
        if not grid.contents[cell]:
            for d in grid.choices(cell):
                conflicts = [0]*10
                for reached,dd in grid.bilocation.reachable(cell,d):
                    if (1L<<reached) & conflicts[dd]:
                        grid.place(d,cell)
                        break
                    else:
                        conflicts[dd] |= neighbors[reached]
                if cell in grid.bivalues:
                    for reached,dd in grid.bivalues.reachable(cell,
                                                grid.otherbv[cell,d]):
                        other = grid.otherbv[reached,dd]
                        if (1L<<reached) & conflicts[other]:
                            grid.place(d,cell)
                            break
                        else:
                            conflicts[other] |= neighbors[reached]

# triples of name, rule, difficulty level
rules = [
    ("locate",locate,0),
    ("eliminate",eliminate,1),
    ("triad",triad,2),
    ("align",align,2),
    ("pair",pair,2),
    ("digit",digit,3),
    ("subproblem",subproblem,3),
    ("rectangle",remotepair,3),
    ("bilocal",bilocal,3),
    ("bivalue",bivalue,3),
    ("repeat",repeat,4),
    ("conflict",conflict,4),
]

def step(grid, quick_and_dirty = False):
    """Try the rules, return True if one succeeds."""
    if grid.complete():
        return False
    grid.progress = False
    for name,rule,level in rules:
        if level <= 1 or not quick_and_dirty:
            rule(grid)
            if grid.progress:
                grid.rules_used.add(name)
                if grid.verbose:
                    print >>sys.stderr,"Rule",name,"made progress"
                return True
    return False

# ======================================================================
#   Random permutation of puzzles
# ======================================================================

def block_permutation(preserve_symmetry = True):
    """Choose order to rearrange rows or columns of blocks."""
    if preserve_symmetry:
        return random.choice([[0,1,2],[2,1,0]])
    result = [0,1,2]
    random.shuffle(result)
    return result

def permute1d(preserve_symmetry = True):
    """Choose order to rearrange rows or columns of puzzle."""
    bp = block_permutation(preserve_symmetry)
    ip = [block_permutation(False),block_permutation(preserve_symmetry)]
    if preserve_symmetry:
        ip.append([2-ip[0][2],2-ip[0][1],2-ip[0][0]])
    else:
        ip.append(block_permutation(False))
    return [bp[i]*3+ip[i][j] for i in [0,1,2] for j in [0,1,2]]

def permute(grid, preserve_symmetry = True):
    """Generate a randomly permuted version of the input puzzle."""
    digit_permutation = list(digits)
    random.shuffle(digit_permutation)
    digit_permutation = [0]+digit_permutation
    row_permutation = permute1d(preserve_symmetry)
    col_permutation = permute1d(preserve_symmetry)
    transpose = random.choice([[1,9],[9,1]])
    contents = [None]*81
    for row in range(9):
        for col in range(9):
            contents[row_permutation[row]*transpose[0] +
                     col_permutation[col]*transpose[1]] = \
                digit_permutation[grid.contents[9*row+col]]
    return Sudoku(contents)

# ======================================================================
#   Output of puzzles
# ======================================================================

# Output functions should return True if it's ok to add difficulty/level,
# false otherwise

def text_format(grid):
    for row in digits:
        if row % 3 != 1:
            print ('|' + ' '*11)*3+'|'
        elif row == 1:
            print ' ' + '-'*35 + ' '
        else:
            print '|' + '-'*35 + '|'
        for col in digits:
            if col % 3 == 1:
                print '|',
            else:
                print ' ',
            print grid.contents[(row-1)*9+(col-1)] or '.',
        print '|'
    print ' ' + '-'*35 + ' '
    return True

def numeric_format(grid):
    row = []
    for digit in grid:
        row.append(str(digit))
        if len(row) == 9:
            print ''.join(row)
            row = []
    return True

def html_format(grid):
    print "<table border=1>"
    for a in range(3):
        print "<tr>"
        for b in range(3):
            print "<td><table border=0>"
            for c in range(3):
                print "<tr>"
                for d in range(3):
                    row = 3*a+c
                    col = 3*b+d
                    cell = 9*row+col
                    if grid.contents[cell]:
                        print '<td width=30 height=30 align=center valign=middle style="font-family:times,serif; font-size:16pt; text-align:center; color:black">%d</td>' % grid.contents[cell]
#                        sty = '; color:black'
#                        val = ' value="%d" readonly' % grid.contents[cell]
                    else:
                        print '<td width=30 height=30 align=center valign=middle><input style="font-family:times,serif; font-size:16pt; text-align:center; color:#555; margin:0pt; border-width:0" size=1 maxlength=1></td>'
#                        sty = '; color:gray'
#                        val = ''
#                    print '<td width=30 height=30 align=center valign=middle><input style="font-size:16pt; text-align:center%s" size=1 maxlength=1%s></td>' % (sty,val)
                print "</tr>"
            print "</table></td>"
        print "</tr>"
    print "</table>"
    return False

def svg_format(grid):
    print '''<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
 "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="274pt" height="274pt" viewBox="0 0 273 273">'''
    print '  <g fill="none" stroke="black" stroke-width="1.5">'
    print '    <rect x="2" y="2" width="270" height="270" />'
    for i in [3,6]:
        print '    <line x1="2" y1="%d" x2="272" y2="%d" />' % (30*i+2,30*i+2)
        print '    <line x1="%d" y1="2" x2="%d" y2="272" />' % (30*i+2,30*i+2)
    print '  </g>'
    print '  <g fill="none" stroke="black" stroke-width="0.5">'
    for i in [1,2,4,5,7,8]:
        print '    <line x1="2" y1="%d" x2="272" y2="%d" />' % (30*i+2,30*i+2)
        print '    <line x1="%d" y1="2" x2="%d" y2="272" />' % (30*i+2,30*i+2)
    print '  </g>'
    print '  <g font-family="Times" font-size="24" fill="black" text-anchor="middle">'
    for row in range(9):
        for col in range(9):
            cell = row*9+col
            if grid.contents[cell]:
                print '    <text x="%d" y="%d">%d</text>' % \
                    (30*col+17, 30*row+25, grid.contents[cell])
    print '  </g>'
    print '</svg>'
    return False

output_formats = {
    "text": text_format,
    "txt": text_format,
    "t": text_format,
    "numeric": numeric_format,
    "num": numeric_format,
    "n": numeric_format,
    "html": html_format,
    "h": html_format,
    "svg": svg_format,
    "s": svg_format,
}
    
# ======================================================================
#   Backtracking search for all solutions
# ======================================================================

def all_solutions(grid):
    """Generate sequence of completed Sudoku grids from initial puzzle."""
    while True:
        # first try the usual non-backtracking rules
        try:
            while step(grid,True): pass
        except BadSudoku:
            return  # no solutions
    
        # if they finished off the puzzle, there's only one solution
        if grid.complete():
            yield grid
            return
        
        # find a cell with few remaining possibilities
        def choices(c):
            ch = grid.choices(c)
            if len(ch) < 2: return (10,0,0)
            return (len(ch),c,ch[0])
        L,c,d = min([choices(c) for c in range(81)])
        
        # try it both ways
        branch = Sudoku(grid)
        if grid.verbose:
            print >>sys.stderr,"Branching in backtracking search"
            branch.verbose = True
        branch.place(d,c)
        for sol in all_solutions(branch):
            yield sol
        if grid.verbose:
            print >>sys.stderr,"Returned from backtracking branch"
        grid.rules_used.update(branch.rules_used)
        grid.rules_used.add("backtrack")
        grid.unplace(d,1L<<c)   #...and loop back to try again

def unisolvent(grid):
    """Does this puzzle have a unique solution?"""
    stream = all_solutions(grid)
    try:
        stream.next()
    except StopIteration:
        return False
    try:
        stream.next()
    except StopIteration:
        return True
    return False

# ======================================================================
#   Command-line interface
# ======================================================================

parser = OptionParser()

parser.add_option("-r","--rules",dest="show_rules", action="store_true",
                  help = "show description of known solver rules and exit")

parser.add_option("-l","--levels",dest="show_levels", action="store_true",
                  help = "show description of difficulty levels and exit")

parser.add_option("-0", "--blank", dest="empty", action="store_true",
                  help = "output blank sudoku grid and exit")

parser.add_option("-t","--translate", dest="translate", action="store_true",
                  help = "translate format of input puzzle without solving")

parser.add_option("-p","--permute",dest="permute", action="store_true",
                  help = "randomly rearrange the input puzzle")

parser.add_option("-g","--generate", dest="generate", action="store_true",
                  help = "generate new puzzle rather than reading from stdin")

parser.add_option("-a", "--asymmetric", dest="asymmetric", action="store_true",
                  help = "allow asymmetry in generated puzzles")

parser.add_option("-b", "--backtrack", dest="backtrack", action="store_true",
                  help = "enable trial and error search for all solutions")

parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help = "output description of each step in puzzle solution")

parser.add_option("-x", "--empty", dest="emptychars", action="store",
                  type="string", default=".0",
                  help="characters representing empty cells in input puzzle")

parser.add_option("-2", "--output-both", dest="output_both",
                  action="store_true",
                  help = "output both the puzzle and its solution")

parser.add_option("-f", "--format", dest="format", action="store",
                  type="string", default="text",
                  help="output format (options: text, numeric, html, svg)")

if __name__ == '__main__':
    options,args = parser.parse_args()
    if args:
        print >>sys.stderr, "Unrecognized command line syntax, use --help for input documentation"
        sys.exit(0)
    
    if options.show_rules:
        print """This solver knows the following rules.  Rules occurring later
in the list are attempted only when all earlier rules have failed
to make progress.
"""
        for name,rule,difficulty in rules:
            print name + ":" + rule.__doc__
        sys.exit(0)

    if options.show_levels:
        print """
Puzzles are classified by difficulty, according to a weighted combination
of the set of rules needed to solve each puzzle.  There are six levels,
in order by difficulty: easy, moderate, tricky, difficult, evil, and
fiendish.  In addition, a puzzle is classified as impossible if this
program cannot find a solution for it, or if backtracking is needed to
find the solution.
"""
        sys.exit(0)

    if options.translate:
        if options.generate:
            print "Can not simultaneously generate and translate puzzles."
            sys.exit(0)
    
    try:
        outputter = output_formats[options.format.lower()]
    except KeyError:
        print "Unrecognized output format."
        sys.exit(0)

    if options.empty:
        outputter(Sudoku())
        sys.exit(0)

# ======================================================================
#   Initial puzzle setup
# ======================================================================

def random_puzzle(generate_symmetric = True):
    """Generate and return a randomly constructed Sudoku puzzle instance."""
    puzzle = []
    grid = Sudoku()

    def choices(cell):
        c = grid.choices(cell)
        return len(c) > 1 and c or []

    while True:
        try:
            while not grid.complete():
                d,c = random.choice([(d,c) for c in range(81)
                                           for d in choices(c)])
                grid.place(d,c)
                while step(grid,True): pass
                puzzle.append((d,c))
                if generate_symmetric:
                    c = 80-c
                    ch = grid.choices(c)
                    if not ch:  # avoid IndexError from random.choice
                        raise BadSudoku("Placement invalidated symmetric cell")
                    d = random.choice(ch)
                    grid.place(d,c)
                    while step(grid,True): pass
                    puzzle.append((d,c))
        except BadSudoku:
            puzzle = []
            grid = Sudoku()
            continue
        break
    
    # find redundant information in initial state
    q = 0
    while q < len(puzzle):
        grid = Sudoku(puzzle[:q] + puzzle[q+1+generate_symmetric:])
        if not unisolvent(grid):
            q += 1+generate_symmetric
        else:
            del puzzle[q]
            if generate_symmetric:
                del puzzle[q]

    return Sudoku(puzzle)

def read_puzzle(empty = ".0"):
    """Read and return a Sudoku instance from standard input."""
    def digits():
        for digit in sys.stdin.read():
            if digit in empty:
                yield 0
            elif '1' <= digit <= '9':
                yield int(digit)
    return Sudoku(digits())

if __name__ == '__main__':
    if options.generate:
        puzzle = random_puzzle(not options.asymmetric)
        print_puzzle = True
        print_solution = options.output_both
    else:
        puzzle = read_puzzle(options.emptychars)
        print_puzzle = options.output_both or options.translate
        print_solution = options.output_both or not options.translate
    if options.permute:
        puzzle = permute(puzzle, not options.asymmetric)
    puzzle.verbose = options.verbose

# ======================================================================
#   Main program: print and solve puzzle
# ======================================================================

if __name__ == '__main__':
    print_level = True
    if print_puzzle:
        print_level = outputter(puzzle)
        
    if options.output_both and print_level:
        print
    
    while step(puzzle): pass
    if options.backtrack:
        solns = all_solutions(puzzle)
    else:
        solns = [puzzle]

    nsolns = 0
    for soln in solns:    
        if print_solution:
            print_level = outputter(soln)
        nsolns += 1

    difficulty = 0
    used_names = []
    for name,rule,level in rules:
        if name in puzzle.rules_used:
            used_names.append(name)
            difficulty += 1<<level
    if "backtrack" in puzzle.rules_used:
        used_names.append("backtrack")
    if print_level:
        print "\nRules used:", ", ".join(used_names)
        if nsolns != 1:
            print "Number of solutions:",nsolns
        if not puzzle.complete() or "backtrack" in puzzle.rules_used:
            print "Level: impossible"
        elif difficulty <= 1:
            print "Level: easy"
        elif difficulty <= 5:
            print "Level: moderate"
        elif difficulty <= 9:
            print "Level: tricky"
        elif difficulty <= 17:
            print "Level: difficult"
        elif difficulty <= 33:
            print "Level: evil"
        else:
            print "Level: fiendish"
