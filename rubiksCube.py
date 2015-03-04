import random, copy

class Face:

    def __init__(self, n, size=3):
        self.size = size
        self.face = [[(n, r, c) for c in range(size)] for r in range(size)]

    def tile(self, row, col):
        return self.face[row][col]

    def col(self, col):
        return [self.face[row][col] for row in range(self.size)]

    def setCol(self, col, newCol):
        for row in range(self.size):
            self.face[row][col] = newCol[row]

    def row(self, row, normalization=(0, 0, 0)):
        rowsToCols, invert, reverse = normalization
        i = self._invertIndex(row) if invert else row
        r = self.col(i) if rowsToCols else self.face[i]
        return r[::-1] if reverse else r

    def setRow(self, row, newRow, normalization=(0, 0, 0)):
        rowsToCols, invert, reverse = normalization
        i = self._invertIndex(row) if invert else row
        newRow = newRow[::-1] if reverse else newRow
        if rowsToCols:
            self.setCol(i, newRow)
        else:
            self.face[i] = newRow

    def _invertIndex(self, i):
        return 0 if i == self.size - 1 else self.size - 1 if i == 0 else 1

    def rotate(self, clockwise=True):
        if clockwise == True:
            self.face = [self.col(c)[::-1] for c in range(self.size)]
        else:
            self.face = [self.col(c) for c in range(self.size)][::-1]

    def __repr__(self):
        s = ''
        for row in range(self.size):
            s += '['
            for col in range(self.size):
                s += str(self.face[row][col]) + ', '
            s = s[:-2] + '],\n'
        return s[:-2]


class Cube:

    # Colors

    GREEN   = 0
    BLUE    = 1
    WHITE   = 2
    YELLOW  = 3
    ORANGE  = 4
    RED     = 5

    F = SIDE_FRONT  = 0
    B = SIDE_BACK   = 1
    U = SIDE_UP     = 2
    D = SIDE_DOWN   = 3
    L = SIDE_LEFT   = 4
    R = SIDE_RIGHT  = 5

    colors = {
        F : GREEN  ,
        B : BLUE   ,
        U : WHITE  ,
        D : YELLOW ,
        L : ORANGE ,
        R : RED
    }

    connections = {
    # Side:  U  D  L  R
        F : (U, D, L, R),
        B : (D, U, L, R),
        U : (B, F, L, R),
        D : (F, B, L, R),
        L : (U, D, B, F),
        R : (U, D, F, B)
    }

    normalizations = {
    # Tuple = (rowsToCols, invertIndexes, reverseRows)
    # **Sides are relative below**
    # Side:  Up         Down       Left       Right
        F : [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)],
        B : [(0, 0, 0), (0, 1, 1), (1, 1, 0), (1, 0, 1)],
        U : [(0, 0, 0), (0, 1, 1), (0, 1, 1), (0, 1, 1)],
        D : [(0, 0, 0), (0, 1, 1), (0, 0, 0), (0, 0, 0)],
        L : [(1, 1, 0), (1, 1, 0), (1, 1, 0), (1, 1, 0)],
        R : [(1, 0, 1), (1, 0, 1), (1, 0, 1), (1, 0, 1)]
    }


    def __init__(self, size=3):
        self.sides = {}
        self.size = size

        self.sides[self.F] = self.front = Face(self.F, size)
        self.sides[self.B] = self.back  = Face(self.B, size)
        self.sides[self.U] = self.up    = Face(self.U, size)
        self.sides[self.D] = self.down  = Face(self.D, size)
        self.sides[self.L] = self.left  = Face(self.L, size)
        self.sides[self.R] = self.right = Face(self.R, size)

        self.pastMoves = []


    def __repr__(self):
        return '\n' \
         +     '\nFront:\n' + str(self.front)   + '\n' \
         +     '\nBack: \n' + str(self.back)    + '\n' \
         +     '\nUp:   \n' + str(self.up)      + '\n' \
         +     '\nDown: \n' + str(self.down)    + '\n' \
         +     '\nLeft: \n' + str(self.left)    + '\n' \
         +     '\nRight:\n' + str(self.right)   + '\n'

    def __eq__(self,other):
        return str(self) == str(other)

    def copy(self):
        return copy.deepcopy(self)

    def entropy(self):
        e = 0
        for side, face in self.sides.iteritems():
            for row in range(self.size):
                for col in range(self.size):
                    e += not ((side, row, col) == face.tile(row, col))
        return e


    def clearMoves(self):
        self.pastMoves = []


    def scramble(self, n):
        sides = [
            self.SIDE_UP, self.SIDE_DOWN,
            self.SIDE_LEFT, self.SIDE_RIGHT,
            self.SIDE_BACK, self.SIDE_FRONT
        ]
        directions = [True, False]
        for i in range(n):
            self.move(random.choice(sides), random.choice(directions))


    def solve(self):
        for move in self.pastMoves[::-1]:
            side, direction = move
            self.move(side, not direction)
            self.clearMoves()


    def colorForTile(self, tile):
        return self.colors[tile[0]]

    def moveSequence(self,moves):
        for m, d in moves:
            self.move(m, d)


    def move(self, side, clockwise=True):
        self.pastMoves += [(side, clockwise)]

        self.sides[side].rotate(clockwise)

        u, d, l, r = self.connections[side]
        normU, normD, normL, normR = self.normalizations[side]

        n = self.size - 1

        if clockwise:
            hold = self.sides[u].row(n, normU)
            self.sides[u].setRow(n, self.sides[l].row(n, normL), normU)
            self.sides[l].setRow(n, self.sides[d].row(n, normD), normL)
            self.sides[d].setRow(n, self.sides[r].row(n, normR), normD)
            self.sides[r].setRow(n, hold, normR)
        else:
            hold = self.sides[u].row(n, normU)
            self.sides[u].setRow(n, self.sides[r].row(n, normR), normU)
            self.sides[r].setRow(n, self.sides[d].row(n, normD), normR)
            self.sides[d].setRow(n, self.sides[l].row(n, normL), normD)
            self.sides[l].setRow(n, hold, normL)
