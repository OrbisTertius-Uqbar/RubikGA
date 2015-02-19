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


## standard config "g","b", "w", "y", "o", "r"
## uses convention (that i just made up...) in which [0][x] index refers to the side closest to F. for opposite side, indices are the same
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
            print self

    def solveCube(self):
        movesMap = {"f":self.f,"b":self.b, "u": self.u, "d":self.d,"r":self.r, "l":self.l}
        for move in reversed(self.pastMoves):
            movesMap[move[0]]() if len(move) == 2 else movesMap[move[0]](False)


    # move front, and so on...
    def f(self, clockwise=True):
        if clockwise==True:
            self.pastMoves += ["f"]
            print "moving front clockwise..."
            hold = [self.R.face[i][0] for i in range(3)]
            self.R.face[0][0]=self.U.face[0][0]
            self.R.face[1][0]=self.U.face[0][1]
            self.R.face[2][0]=self.U.face[0][2]

            self.U.face[0][0]=self.L.face[0][2]
            self.U.face[0][1]=self.L.face[1][2]
            self.U.face[0][2]=self.L.face[2][2]

            self.L.face[0][2]=self.D.face[2][0]
            self.L.face[1][2]=self.D.face[2][1]
            self.L.face[2][2]=self.D.face[2][2]

            self.D.face[2]=hold
        else:
            self.pastMoves += ["f'"]
            print "moving front counter-clockwise..."
            hold = [self.L.face[i][0] for i in range(3)]

            self.L.face[0][2]=self.U.face[0][2]
            self.L.face[1][2]=self.U.face[1][2]
            self.L.face[2][2]=self.U.face[2][2]

            self.U.face[0][0]=self.R.face[0][2]
            self.U.face[0][1]=self.R.face[1][2]
            self.U.face[0][2]=self.R.face[2][2]

            self.R.face[0][2]=self.D.face[0][0]
            self.R.face[1][2]=self.D.face[1][0]
            self.R.face[2][2]=self.D.face[2][0]

            self.D.face[2]=hold



def play():
    c = Cube()
    moves = {"f":c.f,"b":c.b,"u":c.u,"d":c.d, "l":c.l,"r":c.r}
    while True:
        move = raw_input("Enter next move: ")
        if move=="quit":
            print"You've given up..."
            break
        if move == "scramble":
            n = input("How many moves? ")
            c.scrambleCube(n)

        if move == "" or move[0] not in moves:
            print "Invalid move."
        else:
            moves[move[0]]() if len(move)==1 else moves[move[0]](False)
            print c
