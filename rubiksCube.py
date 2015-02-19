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

    # Colors

    GREEN   = 0
    BLUE    = 1
    WHITE   = 2
    YELLOW  = 3
    ORANGE  = 4
    RED     = 5


    # Sides

    SIDE_TOP     = 0
    SIDE_RIGHT   = 1
    SIDE_BOTTOM  = 2
    SIDE_LEFT    = 3
    SIDE_BACK    = 4
    SIDE_FRONT   = 5


    def __init__(self,
        front=GREEN,
        back=BLUE,
        top=WHITE,
        bottom=YELLOW,
        left=ORANGE,
        right=RED):

        self.front  = Face(front)
        self.back   = Face(back)
        self.top    = Face(top)
        self.bottom = Face(bottom)
        self.left   = Face(left)
        self.right  = Face(right)

        self.pastMoves = []


    def __repr__(self):
        front   = "\nFront: \n"+str(self.front) + "\n\n"
        back    = "Back: \n"+str(self.back)+"\n\n"
        up      = "Top: \n"+str(self.top)+"\n\n"
        down    = "Bottom: \n"+ str(self.bottom) +"\n\n"
        left    = "Left: \n"+str(self.left)+"\n\n"
        right   = "Right: \n"+str(self.right)+"\n"
        return front + back + up + down + left + right


    def clearMoves(self):
        self.pastMoves = []


    def scrambleCube(self, n):
        sides = [
            self.SIDE_TOP, self.SIDE_BOTTOM,
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
            if clockwise==True:
                print "moving front clockwise..."
                hold = self.right.getColumn(0)
                self.right.setColumn(0, self.top.getRow(2))
                self.top.setRow(2, self.left.getColumn(2))
                self.left.setColumn(2, self.bottom.getRow(0))
                self.bottom.setRow(0,hold)

            else:
                print "moving front counter-clockwise..."
                hold = self.left.getColumn(2)
                self.left.setColumn(2, self.top.getRow(2))
                self.top.setRow(2, self.right.getColumn(0))
                self.right.setColumn(0, self.bottom.getRow(0))
                self.bottom.setRow(0, hold)

        elif side is self.SIDE_BACK:
            if clockwise==True:
                print "moving back clockwise..."
                hold = self.right.getColumn(2)
                self.right.setColumn(2,self.bottom.getRow(2))
                self.bottom.setRow(2, self.left.getColumn(0))
                self.left.setColumn(0,self.top.getRow(0))
                self.top.setRow(0,hold)
            else:
                print "moving back counter-clockwise"
                hold = self.left.getColumn(0)
                self.left.setColumn(0,self.bottom.getRow(2))
                self.bottom.setRow(2, self.right.getColumn(2))
                self.right.setColumn(2,self.top.getRow(0))
                self.top.setRow(0,hold)

        elif side is self.SIDE_LEFT:
            if clockwise==True:
                print "moving left clockwise..."
                hold = self.top.getColumn(0)
                self.top.setColumn(0,self.back.getColumn(0))
                self.back.setColumn(0,self.bottom.getColumn(0))
                self.bottom.setColumn(0, self.front.getColumn(0))
                self.front.setColumn(0,hold)
            else:
                print "moving left counter-clockwise"
                hold = self.bottom.getColumn(0)
                self.bottom.setColumn(0, self.back.getColumn(0))
                self.back.setColumn(0 ,self.top.getColumn(0))
                self.top.setColumn(0,self.front.getColumn(0))
                self.front.setColumn(0,hold)

        elif side is self.SIDE_RIGHT:
            if clockwise==True:
                print "moving right clockwise..."
                hold = self.top.getColumn(2)
                self.top.setColumn(2,self.back.getColumn(2))
                self.back.setColumn(2,self.bottom.getColumn(2))
                self.bottom.setColumn(2, self.front.getColumn(2))
                self.front.setColumn(2,hold)
            else:
                print "moving right counter-clockwise"
                hold = self.bottom.getColumn(2)
                self.bottom.setColumn(2,self.back.getColumn(2))
                self.back.setColumn(2,self.top.getColumn(2))
                self.top.setColumn(2,self.front.getColumn(2))
                self.front.setColumn(2,hold)


        elif side is self.SIDE_BOTTOM:
            if clockwise==True:
                print "moving bottom clockwise..."
                hold = self.right.getRow(2)
                self.right.setRow(2,self.front.getRow(2))
                self.front.setRow(2,self.left.getRow(2))
                self.left.setRow(2, self.back.getRow(2))
                self.back.setRow(2,hold)
            else:
                print "moving bottom counter-clockwise"
                hold = self.left.getRow(2)
                self.left.setRow(2, self.front.getRow(2))
                self.front.setRow(2,self.right.getRow(2))
                self.right.setRow(2,self.back.getRow(2))
                self.back.setRow(2,hold)

        elif side is self.SIDE_TOP:
            if clockwise==True:
                print "moving top clockwise..."
                hold = self.right.getRow(0)
                self.right.setRow(0,self.front.getRow(0))
                self.front.setRow(0,self.left.getRow(0))
                self.left.setRow(0, self.back.getRow(0))
                self.back.setRow(0,hold)
            else:
                print "moving top counter-clockwise"
                hold = self.left.getRow(0)
                self.left.setRow(0, self.front.getRow(0))
                self.front.setRow(0,self.right.getRow(0))
                self.right.setRow(0,self.back.getRow(0))
                self.back.setRow(0,hold)
