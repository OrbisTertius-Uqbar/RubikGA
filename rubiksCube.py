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

    def rotateFace(self, clockwise=True):
        if clockwise == True:
            self.face = [self.getColumn(0)[::-1],self.getColumn(1)[::-1],self.getColumn(2)[::-1]]
        else:
            self.face = [self.getColumn(2),self.getColumn(1),self.getColumn(0)]




class Cube:

    # Colors

    GREEN   = 0
    BLUE    = 1
    WHITE   = 2
    YELLOW  = 3
    ORANGE  = 4
    RED     = 5


    # Sides

    SIDE_UP     = 0
    SIDE_RIGHT   = 1
    SIDE_DOWN  = 2
    SIDE_LEFT    = 3
    SIDE_BACK    = 4
    SIDE_FRONT   = 5


    def __init__(self,
        front=GREEN,
        back=BLUE,
        up=WHITE,
        down=YELLOW,
        left=ORANGE,
        right=RED):

        self.front  = Face(front)
        self.back   = Face(back)
        self.up    = Face(up)
        self.down = Face(down)
        self.left   = Face(left)
        self.right  = Face(right)

        self.pastMoves = []


    def __repr__(self):
        front   = "\nFront: \n"+str(self.front) + "\n\n"
        back    = "Back: \n"+str(self.back)+"\n\n"
        up      = "up: \n"+str(self.up)+"\n\n"
        down    = "down: \n"+ str(self.down) +"\n\n"
        left    = "Left: \n"+str(self.left)+"\n\n"
        right   = "Right: \n"+str(self.right)+"\n"
        return front + back + up + down + left + right


    def clearMoves(self):
        self.pastMoves = []


    def scrambleCube(self, n):
        sides = [
            self.SIDE_UP, self.SIDE_DOWN,
            self.SIDE_LEFT, self.SIDE_RIGHT,
            self.SIDE_BACK, self.SIDE_FRONT
        ]
        directions = [True, False]
        for i in range(n):
            self.move(random.choice(sides), random.choice(directions))


    def solveCube(self):
        for move in self.pastMoves[::-1]:
            side, direction = move
            self.move(side, not direction)
            self.clearMoves()


    def move(self, side, clockwise=True):
        self.pastMoves += [(side, clockwise)]


        if side is self.SIDE_FRONT:

            self.front.rotateFace(clockwise)

            if clockwise==True:
                print "moving front clockwise..."
                hold = self.right.getColumn(0)
                self.right.setColumn(0, self.up.getRow(2))
                self.up.setRow(2, self.left.getColumn(2))
                self.left.setColumn(2, self.down.getRow(0))
                self.down.setRow(0,hold)



            else:
                print "moving front counter-clockwise..."
                hold = self.left.getColumn(2)
                self.left.setColumn(2, self.up.getRow(2))
                self.up.setRow(2, self.right.getColumn(0))
                self.right.setColumn(0, self.down.getRow(0))
                self.down.setRow(0, hold)

        elif side is self.SIDE_BACK:
            self.back.rotateFace(clockwise)

            if clockwise==True:
                print "moving back clockwise..."
                hold = self.right.getColumn(2)
                self.right.setColumn(2,self.down.getRow(2))
                self.down.setRow(2, self.left.getColumn(0))
                self.left.setColumn(0,self.up.getRow(0))
                self.up.setRow(0,hold)
            else:
                print "moving back counter-clockwise"
                hold = self.left.getColumn(0)
                self.left.setColumn(0,self.down.getRow(2))
                self.down.setRow(2, self.right.getColumn(2))
                self.right.setColumn(2,self.up.getRow(0))
                self.up.setRow(0,hold)

        elif side is self.SIDE_LEFT:
            self.left.rotateFace(clockwise)
            if clockwise==True:
                print "moving left clockwise..."
                hold = self.up.getColumn(0)
                self.up.setColumn(0,self.back.getColumn(0))
                self.back.setColumn(0,self.down.getColumn(0))
                self.down.setColumn(0, self.front.getColumn(0))
                self.front.setColumn(0,hold)
            else:
                print "moving left counter-clockwise"
                hold = self.down.getColumn(0)
                self.down.setColumn(0, self.back.getColumn(0))
                self.back.setColumn(0 ,self.up.getColumn(0))
                self.up.setColumn(0,self.front.getColumn(0))
                self.front.setColumn(0,hold)

        elif side is self.SIDE_RIGHT:
            self.right.rotateFace(clockwise)
            if clockwise==True:
                print "moving right clockwise..."
                hold = self.down.getColumn(2)
                self.down.setColumn(2,self.back.getColumn(2))
                self.back.setColumn(2,self.up.getColumn(2))
                self.up.setColumn(2,self.front.getColumn(2))
                self.front.setColumn(2,hold)

            else:
                print "moving right counter-clockwise"
                hold = self.up.getColumn(2)
                self.up.setColumn(2,self.back.getColumn(2))
                self.back.setColumn(2,self.down.getColumn(2))
                self.down.setColumn(2, self.front.getColumn(2))
                self.front.setColumn(2,hold)


        elif side is self.SIDE_DOWN:
            self.down.rotateFace(clockwise)
            if clockwise==True:
                print "moving down clockwise..."
                hold = self.right.getRow(2)
                self.right.setRow(2,self.front.getRow(2))
                self.front.setRow(2,self.left.getRow(2))
                self.left.setRow(2, self.back.getRow(2))
                self.back.setRow(2,hold)

            else:
                print "moving down counter-clockwise"
                hold = self.left.getRow(2)
                self.left.setRow(2, self.front.getRow(2))
                self.front.setRow(2,self.right.getRow(2))
                self.right.setRow(2,self.back.getRow(2))
                self.back.setRow(2,hold)

        elif side is self.SIDE_UP:
            self.up.rotateFace(clockwise)
            if clockwise==True:
                print "moving up clockwise..."
                hold = self.right.getRow(0)
                self.right.setRow(0,self.front.getRow(0))
                self.front.setRow(0,self.left.getRow(0))
                self.left.setRow(0, self.back.getRow(0))
                self.back.setRow(0,hold)
            else:
                print "moving up counter-clockwise"
                hold = self.left.getRow(0)
                self.left.setRow(0, self.front.getRow(0))
                self.front.setRow(0,self.right.getRow(0))
                self.right.setRow(0,self.back.getRow(0))
                self.back.setRow(0,hold)
