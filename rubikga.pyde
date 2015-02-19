from rubiksCube import Cube

c = Cube()

def setup():
    size(400, 400, OPENGL)

def drawFace(f):
    # build face
    x = 0
    y = 0
    for i in range(3):
        for j in range(3):
            r,g,b=getColor(f.face[i][j])
            fill(r,g,b)
            rect(x, y, 200 / 3., 200 / 3.)
            x += 200 / 3.
        x = 0
        y += 200 / 3.

## converts string to rgb vals
def getColor(c):
    if c == Cube.RED:
        return 250, 0, 0
    if c == Cube.GREEN:
        return 0, 250, 0
    if c == Cube.ORANGE:
        return 252, 113, 20
    if c == Cube.BLUE:
        return 0, 0, 250
    if c == Cube.YELLOW:
        return 250, 237, 28
    if c == Cube.WHITE:
        return 250, 250, 250



def draw():
    rotationY = mouseX / (float(width) / 2) * TWO_PI
    rotationX = mouseY / (float(height) / 2) * TWO_PI * -1

    background(0)

    rectMode(CORNER)

    translate(200, 200, -100)
    rotateY(rotationY)
    rotateX(rotationX)

    pushMatrix()
    translate(-100, -100, 100)

    # front
    drawFace(c.F)

    # left
    pushMatrix()
    translate(0, 0, -200)
    rotateY(-HALF_PI)
    drawFace(c.L)
    popMatrix()

    # top
    pushMatrix()
    rotateX(-HALF_PI)
    drawFace(c.U)
    popMatrix()

    # right
    pushMatrix()
    translate(200, 0, 0)
    rotateY(HALF_PI)
    drawFace(c.R)
    popMatrix()

    # bottom
    pushMatrix()
    translate(0, 200, -200)
    rotateX(HALF_PI)
    drawFace(c.D)
    popMatrix()

    # back
    pushMatrix()
    translate(0, 0, -200)
    rotateX(TWO_PI)
    drawFace(c.B)
    popMatrix()

    popMatrix()

def keyPressed():
        if  key == "f":
            c.f()
            redraw()

        elif  key == "F":
            c.f(False)
            redraw()

        elif key == "b":
            c.b()
            redraw()
        elif key == "B":
            c.b(False)
            redraw()
        elif key == "l":
            c.l()
            redraw()
        elif key == "L":
            c.l(False)
            redraw()
        elif key == "r":
            c.r()
            redraw()
        elif key == "R":
            c.r(False)
            redraw()
        elif key == "u":
            c.u()
            redraw()
        elif key == "U":
            c.u(False)
            redraw()
        elif key == "d":
            c.d()
            redraw()
        elif key == "D":
            c.d(False)
            redraw()
        elif key == "s":
            c.scrambleCube(50)
            redraw()
        elif  key == "c":
            c.solveCube()
            redraw()
