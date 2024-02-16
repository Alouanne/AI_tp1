## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}
import math
import random

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]



digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in squares)


################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')


################ Parse a Grid ################

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  ## (Fail if we can't assign d to square s.)
    return values


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


################ Constraint Propagation ################

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  ## Already eliminated
    values[s] = values[s].replace(d, '')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


################ Display as 2-D grid ################

def display(values):
    "Display these values as a 2-D grid."
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else ''))
              for c in cols)
        if r in 'CF': print(line)


################ Search ################

def solve(grid): return search(parse_grid(grid))


def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  ## Solved!
    num = 0
    for s in squares:
        num = num + len(values[s])

    values = simulated_annealing(values)

    return values
    #if (num/len(values) > 3):
     #   values = nacked_Pair(values)
      #  if all(len(values[s]) == 1 for s in squares):
       #     return values  ## Solved!
    # random choice
    # s = random.choice(squares)
    # while len(s) == 1:
    #    s = random.choice(squares)
    # locked canididates
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    try:
        return some(search(assign(values.copy(), s, d))
                for d in values[s])
    except:
        return values

def hidden_singles(values):
    num = '123456789'
    for unit in unitlist:

        for lip in num:
            places = ""
            for s in unit:
                if (lip in values[s]):
                    places = s
            if (len(places) == 1):
                if not assign(values, places[0], lip):
                    return False
    return values
def hillClimbingSetup(values):
    unit = 18
    valuesOri = values.copy()
    while(unit < 27):
        skip=0
        num = 0
        while (num < 9 and skip ==0):
            loop = 0
            numb = 0
            while (numb < 9 and skip ==0):
                if (len(values[unitlist[unit][numb]]) != 1):
                    loop = 1
                numb = numb + 1

            if (loop == 0):
                skip = 1
            loop = 0
            p = unitlist[unit]
            try:
                n, s = min((len(values[s]), s) for s in p if len(values[s]) > 1)

                if(len(values[s]) != 1):
                    val = values[s][1]

                    while(loop < 9 and skip == 0):

                        if(p[loop] != s and len(values[p[loop]]) != 1):
                            values[p[loop]] = values[p[loop]].replace(val, '')

                            if (len(values[p[loop]]) == 1):
                                looper = 0
                                while (looper < 9 ):
                                    if (p[looper] != p[loop]):
                                        values[p[looper]] = values[p[looper]].replace(values[p[loop]], '')

                                    looper = looper + 1
                        else:
                            values[s] = val

                        loop = loop+1
                num = num+1
            except:
                skip = 1

        unit = unit + 1
    #print("start")
    hillClimbingChecker(values, valuesOri)
    #print(values)
    return values

def hillClimbingChecker(values, ValOrigi):
    base = conflictCheck(values)
    num = 0
    numk = 0
    tab = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    unit = [0,1,2,3,4,5,6,7,8]
    if(base == 0 ):
        print("Succes")
        return values
    else:
        num = 0
        while(numk < 1):
            bs = 0
            for a in unit:

                num = 0
                while(num < 1000):
                    b = random.choice(unit)
                    c = random.choice(unit)
                    #print(num, a,b,c)


                    if(c < b and len(ValOrigi[unitlist[a][c]]) != 1 and len(ValOrigi[unitlist[a][b]]) != 1 and (tab[b][c] == 0 or tab[c][b] == 0)):
                        tab[b][c] = 1
                        tab[c][b] = 1
                        bs = 1
                        try:
                            valuesBack = values.copy()
                        except:
                            return values
                        valuesBack[unitlist[a][b]],valuesBack[unitlist[a][c]]  = values[unitlist[a][c]], values[unitlist[a][b]]
                        newB = conflictCheck(valuesBack)
                        #print(newB, base)
                        if(newB < base):
                            #print("better", newB)
                            values = hillClimbingChecker(valuesBack, ValOrigi)
                            base = conflictCheck(values)
                    else:
                        if(len(ValOrigi[unitlist[a][b]]) == 1 and len(ValOrigi[unitlist[a][c]]) == 1):
                            tab[b][c] = 2
                            tab[c][b] = 2
                    num = num + 1

                if(bs==0 and a == 8):
                    numk = numk + 1

    return values



def simulated_annealing(values):
    current_values = values.copy()
    current_conflict = conflictCheck(current_values)
    T = 3.0  
    T_min = 0.1  
    alpha = 0.99  
    while T > T_min:
        i = 0
        while i <= 100:
            new_values = current_values.copy()
            # selectionner deux cases dans un carre au hasard et on les echange
            square = random.choice(unitlist[18:])  # choisir que parmis les carres 3x3
            s1, s2 = random.sample(square, 2)
            # Échanger les valeurs
            new_values[s1], new_values[s2] = new_values[s2], new_values[s1]
            new_conflict = conflictCheck(new_values)
            # on calcule la difference de conflits
            delta = new_conflict - current_conflict
            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / T):
                current_values = new_values.copy()
                current_conflict = new_conflict
            i += 1
        T = T * alpha  # Diminuer la température
    return current_values




def conflictCheck(values):
    conflict = 0
    for x in rows:
        for y in digits:
            for i in rows:
                for k in digits:
                    if(y == k or x == i):
                        if(y > k or x > i):
                            xy = x + y
                            ij = i + k
                            if(values[xy] == values[ij]):

                                conflict = conflict + 1
    #print(conflict)
    return conflict

def nacked_Pair(values):
    results = [0]
    num = 0

    square = unitlist
    while (num < 27):
        for k in square[num]:
            for s in square[num]:
                if (len(values[s]) == 2 and len(values[k]) == 2):
                    if s != k:
                        if values[s] == values[k]:
                            for x in square[num]:
                                if (x != s and x != k):
                                    i = 0
                                    while (i < len(values[s])):
                                        if(len(values[x]) != 1):
                                            eliminate(values, x, values[s][i])
                                        i = i + 1

        num = num + 1

    return values


################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False


def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return open(filename).read().strip().split(sep)


def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq


################ System test ################

import time, random


def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""

    def time_solve(grid):
        start = time.process_time()
        values = solve(grid)
        t = time.process_time() - start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times) / N, N / sum(times), max(times)))


def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    nackedPair = False

    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)

    return values is not False and all(unitsolved(unit) for unit in unitlist)


def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s]) == 1 else '.' for s in squares)
    return random_puzzle(N)  ## Give up and make a new puzzle


grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1 = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

if __name__ == '__main__':
    test()
    solve_all(from_file("top95.txt"), "95sudoku", None)
    #solve_all(from_file("easy50.txt", '========'), "easy", None)
    # solve_all(from_file("easy50.txt", '========'), "easy", None)
    solve_all(from_file("100sudoku.txt"), "mid", None)
    # solve_all(from_file("hardest.txt"), "hardest", None)
    solve_all(from_file("1000sudoku.txt"), "hard", None)

## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/
