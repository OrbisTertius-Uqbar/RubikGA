import random

class Face:

    def __init__(self,c):
        self.face = [[c]*3 for i in range(3)]

    def __repr__(self):
        t = self.face[0]
        m = self.face[1]
        b = self.face[2]
        return str(t) + "\n" + str(m) + "\n" + str(b)

    def getColumn(self, col):
        return [self.face[r][col] for r in range(3)]

    def getRow(self, row):
        return self.face[row]

    def setColumn(self, col, newCol):
        for row in range(3):
            self.face[row][col] = newCol[row]

    def setRow(self, row, newRow):
        self.face[row] = newRow


class Cube:

    GREEN = "g"
    BLUE = "b"
    WHITE = "w"
    YELLOW = "y"
    ORANGE = "o"
    RED = "r"

    def __init__(self,
        F=GREEN,
        B=BLUE,
        U=WHITE,
        D=YELLOW,
        L=ORANGE,
        R=RED):

        self.F = Face(F)
        self.B = Face(B)
        self.U = Face(U)
        self.D = Face(D)
        self.L = Face(L)
        self.R = Face(R)

        self.pastMoves = []

    def __repr__(self):
        front= "\nFront: \n"+str(self.F) + "\n\n"
        back = "Back: \n"+str(self.B)+"\n\n"
        up = "Up: \n"+str(self.U)+"\n\n"
        down = "Down: \n"+ str(self.D) +"\n\n"
        left = "Left: \n"+str(self.L)+"\n\n"
        right = "Right: \n"+str(self.R)+"\n"
        return front + back + up + down + left + right

    def clearMoves(self):
        self.pastMoves = []

    def scrambleCube(self, n):
        moves = [self.f, self.b, self.u, self.d, self.l,self.r]
        directions = [True, False]
        for i in range(n):
            random.choice(moves)(random.choice(directions))

    def solveCube(self):
        movesMap = {"f":self.f,"b":self.b, "u": self.u, "d":self.d,"r":self.r, "l":self.l}
        for move in reversed(self.pastMoves):
            movesMap[move[0]]() if len(move) == 2 else movesMap[move[0]](False)
            self.clearMoves()


    # move front, and so on...
    def f(self, clockwise=True):
        if clockwise==True:
            self.pastMoves += ["f"]
            print "moving front clockwise..."
            hold = self.R.getColumn(0)
            self.R.setColumn(0, self.U.getRow(2))
            self.U.setRow(2, self.L.getColumn(2))
            self.L.setColumn(2, self.D.getRow(0))
            self.D.setRow(0,hold)

        else:
            self.pastMoves += ["f'"]
            print "moving front counter-clockwise..."
            hold = self.L.getColumn(2)
            self.L.setColumn(2, self.U.getRow(2))
            self.U.setRow(2, self.R.getColumn(0))
            self.R.setColumn(0, self.D.getRow(0))
            self.D.setRow(0, hold)

    def b(self, clockwise=True):
        if clockwise==True:
            print "moving back clockwise..."
            self.pastMoves +=["b"]
            hold = self.R.getColumn(2)
            self.R.setColumn(2,self.D.getRow(2))
            self.D.setRow(2, self.L.getColumn(0))
            self.L.setColumn(0,self.U.getRow(0))
            self.U.setRow(0,hold)
        else:
            print "moving back counter-clockwise"
            self.pastMoves += ["b'"]
            hold = self.L.getColumn(0)
            self.L.setColumn(0,self.D.getRow(2))
            self.D.setRow(2, self.R.getColumn(2))
            self.R.setColumn(2,self.U.getRow(0))
            self.U.setRow(0,hold)

    def l(self, clockwise=True):
        if clockwise==True:
            print "moving left clockwise..."
            self.pastMoves +=["l"]
            hold = self.U.getColumn(0)
            self.U.setColumn(0,self.B.getColumn(0))
            self.B.setColumn(0,self.D.getColumn(0))
            self.D.setColumn(0, self.F.getColumn(0))
            self.F.setColumn(0,hold)
        else:
            print "moving left counter-clockwise"
            self.pastMoves += ["l'"]
            hold = self.D.getColumn(0)
            self.D.setColumn(0, self.B.getColumn(0))
            self.B.setColumn(0 ,self.U.getColumn(0))
            self.U.setColumn(0,self.F.getColumn(0))
            self.F.setColumn(0,hold)

    def r(self, clockwise=True):
        if clockwise==True:
            print "moving right clockwise..."
            self.pastMoves +=["r"]
            hold = self.D.getColumn(2)
            self.D.setColumn(2,self.B.getColumn(2))
            self.B.setColumn(2,self.U.getColumn(2))
            self.U.setColumn(2,self.F.getColumn(2))

        else:
            print "moving right counter-clockwise"
            self.pastMoves += ["r'"]

            self.F.setColumn(2,hold)
            hold = self.U.getColumn(2)
            self.U.setColumn(2,self.B.getColumn(2))
            self.B.setColumn(2,self.D.getColumn(2))
            self.D.setColumn(2, self.F.getColumn(2))
            self.F.setColumn(2,hold)


    def d(self, clockwise=True):
        if clockwise==True:
            print "moving down clockwise..."
            self.pastMoves +=["d"]
            hold = self.R.getRow(2)
            self.R.setRow(2,self.F.getRow(2))
            self.F.setRow(2,self.L.getRow(2))
            self.L.setRow(2, self.B.getRow(2))
            self.B.setRow(2,hold)
        else:
            print "moving down counter-clockwise"
            self.pastMoves += ["d'"]
            hold = self.L.getRow(2)
            self.L.setRow(2, self.F.getRow(2))
            self.F.setRow(2,self.R.getRow(2))
            self.R.setRow(2,self.B.getRow(2))
            self.B.setRow(2,hold)

    def u(self, clockwise=True):
        if clockwise==True:
            print "moving up clockwise..."
            self.pastMoves +=["u"]
            hold = self.R.getRow(0)
            self.R.setRow(0,self.F.getRow(0))
            self.F.setRow(0,self.L.getRow(0))
            self.L.setRow(0, self.B.getRow(0))
            self.B.setRow(0,hold)
        else:
            print "moving back counter-clockwise"
            self.pastMoves += ["u'"]
            hold = self.L.getRow(0)
            self.L.setRow(0, self.F.getRow(0))
            self.F.setRow(0,self.R.getRow(0))
            self.R.setRow(0,self.B.getRow(0))
            self.B.setRow(0,hold)
