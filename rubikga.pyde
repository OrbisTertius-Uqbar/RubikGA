from rubiksCube import Cube
import math

c = Cube()

canvasSize = 600
cubeSize = math.floor(math.sqrt((canvasSize ** 2) / 2)) * 2

def setup():
    size(canvasSize, canvasSize, OPENGL)


def drawFace(f):
    x, y = (0, 0)
    for row in range(3):
        for col in range(3):
            fill( getColor( f.face[row][col] ) )
            rect(x, y, cubeSize / 3., cubeSize / 3.)
            x += cubeSize / 3.
        x = 0
        y += cubeSize / 3.

# Converts Cube.COLOR to processing color
def getColor(c):
    if c == Cube.RED:
        return color(250, 0, 0)
    if c == Cube.GREEN:
        return color(0, 250, 0)
    if c == Cube.ORANGE:
        return color(252, 113, 20)
    if c == Cube.BLUE:
        return color(0, 0, 250)
    if c == Cube.YELLOW:
        return color(250, 237, 28)
    if c == Cube.WHITE:
        return color(250, 250, 250)


def draw():

    rotationY = mouseX / (float(width) / 2) * TWO_PI
    rotationX = mouseY / (float(height) / 2) * TWO_PI * -1

    background(0)

    rectMode(CORNER)

    halfCubeSize = cubeSize / 2

    translate(canvasSize / 2, canvasSize / 2, -1.3 * cubeSize)
    rotateY(rotationY)
    rotateX(rotationX)

    pushMatrix()
    translate(-halfCubeSize, -halfCubeSize, halfCubeSize)

    # front
    drawFace(c.front)

    # left
    pushMatrix()
    translate(0, 0, -cubeSize)
    rotateY(-HALF_PI)
    drawFace(c.left)
    popMatrix()

    # top
    pushMatrix()
    translate(0, 0, -cubeSize)
    rotateX(HALF_PI)
    drawFace(c.top)
    popMatrix()

    # right
    pushMatrix()
    translate(cubeSize, 0, 0)
    rotateY(HALF_PI)
    drawFace(c.right)
    popMatrix()

    # bottom
    pushMatrix()
    translate(0, cubeSize, 0)
    rotateX(-HALF_PI)
    drawFace(c.bottom)
    popMatrix()

    # back
    pushMatrix()
    translate(0, 0, -cubeSize)
    rotateX(TWO_PI)
    drawFace(c.back)
    popMatrix()

    popMatrix()


def keyPressed():

        clockwise = True
        side = None

        if  key == "f":
            side = Cube.SIDE_FRONT

        elif  key == "F":
            side = Cube.SIDE_FRONT
            clockwise = False

        elif key == "b":
            side = Cube.SIDE_BACK

        elif key == "B":
            side = Cube.SIDE_BACK
            clockwise = False

        elif key == "l":
            side = Cube.SIDE_LEFT

        elif key == "L":
            side = Cube.SIDE_LEFT
            clockwise = False

        elif key == "r":
            side = Cube.SIDE_RIGHT

        elif key == "R":
            side = Cube.SIDE_RIGHT
            clockwise = False

        elif key == "u" or key == "t":
            side = Cube.SIDE_TOP

        elif key == "U" or key == "T":
            side = Cube.SIDE_TOP
            clockwise = False

        elif key == "d":
            side = Cube.SIDE_BOTTOM

        elif key == "D":
            side = Cube.SIDE_BOTTOM
            clockwise = False

        if side != None:
            c.move(side, clockwise)
            return


        # Otherwise...

        if key == "s":
            c.scrambleCube(50)

        elif  key == "c":
            c.solveCube()
