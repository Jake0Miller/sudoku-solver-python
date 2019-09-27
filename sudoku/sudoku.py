from itertools import product

def solve_sudoku(dimensions, board):
    # dimensions are size of each box, not the total grid!
    nRows, nCols = dimensions
    size = nRows * nCols

    X = ([("rc", rc) for rc in product(range(size), range(size))] +
         [("rn", rn) for rn in product(range(size), range(1, size + 1))] +
         [("cn", cn) for cn in product(range(size), range(1, size + 1))] +
         [("bn", bn) for bn in product(range(size), range(1, size + 1))])

    Y = dict()

    for row, col, n in product(range(size), range(size), range(1, size + 1)):
        box = (row // nRows) * nRows + (col // nCols)
        Y[(row, col, n)] = [
            ("rc", (row, col)),
            ("rn", (row, n)),
            ("cn", (col, n)),
            ("bn", (box, n))]

    X, Y = exact_cover(X, Y)

    for i, row in enumerate(board):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))

    for solution in solve(X, Y, []):
        for (row, col, n) in solution:
            board[row][col] = n
        yield board

def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y

def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

if __name__ == "__main__":
    solve_sudoku(dimensions, board)
