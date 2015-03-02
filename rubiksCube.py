import random

class Face:

    def __init__(self, n):
        self.face = [[(n, r, c) for c in range(3)] for r in range(3)]

    def tile(self, row, col):
        return self.face[row][col]

    def col(self, col):
        return [self.face[row][col] for row in range(3)]

    def row(self, row, normalization=(0, 0, 0)):
        rowsToCols, invert, reverse = normalization
        i = row if not invert else 0 if row == 2 else 2 if row == 0 else 1
        r = self.col(i) if rowsToCols else self.face[i]
        return r[::-1] if reverse else r

    def setCol(self, col, newCol):
        for row in range(3):
            self.face[row][col] = newCol[row]

    def setRow(self, row, newRow, normalization=(0, 0, 0)):
        rowsToCols, invert, reverse = normalization
        i = row if not invert else 0 if row == 2 else 2 if row == 0 else 1
        newRow = newRow[::-1] if reverse else newRow
        if rowsToCols:
            self.setCol(i, newRow)
        else:
            self.face[i] = newRow

    def rotate(self, clockwise=True):
        if clockwise == True:
            self.face = [
                self.col(0)[::-1], self.col(1)[::-1], self.col(2)[::-1]
            ]
        else:
            self.face = [self.col(2), self.col(1), self.col(0)]

    def __repr__(self):
        s = ''
        for row in range(3):
            s += '['
            for col in range(3):
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


    def __init__(self):
        self.sides = {}

        self.sides[self.F] = self.front = Face(self.F)
        self.sides[self.B] = self.back  = Face(self.B)
        self.sides[self.U] = self.up    = Face(self.U)
        self.sides[self.D] = self.down  = Face(self.D)
        self.sides[self.L] = self.left  = Face(self.L)
        self.sides[self.R] = self.right = Face(self.R)

        self.pastMoves = []


    def __repr__(self):
        return '\n' \
         +     '\nFront:\n' + str(self.front)   + '\n' \
         +     '\nBack: \n' + str(self.back)    + '\n' \
         +     '\nUp:   \n' + str(self.up)      + '\n' \
         +     '\nDown: \n' + str(self.down)    + '\n' \
         +     '\nLeft: \n' + str(self.left)    + '\n' \
         +     '\nRight:\n' + str(self.right)   + '\n'


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


    def move(self, side, clockwise=True):
        self.pastMoves += [(side, clockwise)]

        self.sides[side].rotate(clockwise)

        u, d, l, r = self.connections[side]
        normU, normD, normL, normR = self.normalizations[side]

        if clockwise:
            hold = self.sides[u].row(2, normU)
            self.sides[u].setRow(2, self.sides[l].row(2, normL), normU)
            self.sides[l].setRow(2, self.sides[d].row(2, normD), normL)
            self.sides[d].setRow(2, self.sides[r].row(2, normR), normD)
            self.sides[r].setRow(2, hold, normR)
        else:
            hold = self.sides[u].row(2, normU)
            self.sides[u].setRow(2, self.sides[r].row(2, normR), normU)
            self.sides[r].setRow(2, self.sides[d].row(2, normD), normR)
            self.sides[d].setRow(2, self.sides[l].row(2, normL), normD)
            self.sides[l].setRow(2, hold, normL)
