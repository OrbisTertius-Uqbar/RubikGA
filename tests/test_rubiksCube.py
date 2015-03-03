# Run like this: python -m unittest discover tests -v

import unittest, rubiksCube, copy

class TestFace(unittest.TestCase):

    def test_faceInit(self):
        face1 = rubiksCube.Face(1)
        face4 = rubiksCube.Face(4)
        self.assertEqual(face1.face,[
            [(1, 0, 0), (1, 0, 1), (1, 0, 2)],
            [(1, 1, 0), (1, 1, 1), (1, 1, 2)],
            [(1, 2, 0), (1, 2, 1), (1, 2, 2)]
        ], 'face #1 incorrectly initialized')
        self.assertEqual(face4.face,[
            [(4, 0, 0), (4, 0, 1), (4, 0, 2)],
            [(4, 1, 0), (4, 1, 1), (4, 1, 2)],
            [(4, 2, 0), (4, 2, 1), (4, 2, 2)]
        ], 'face #4 incorrectly initialized')

    def test_faceColRow(self):
        face = rubiksCube.Face(0)

        self.assertEqual(
            face.row(1),
            [(0, 1, 0), (0, 1, 1), (0, 1, 2)],
            'face.row returned unexpected value for row'
        )
        self.assertEqual(
            face.col(1),
            [(0, 0, 1), (0, 1, 1), (0, 2, 1)],
            'face.col returned unexpected value for column'
        )

        new = [0, 1, 2]
        face.setRow(0, new)
        self.assertEqual(new, face.row(0),
            'face.setRow did not work properly')
        face.setCol(0, new)
        self.assertEqual(new, face.col(0),
            'face.setCol did not work properly')

    def test_rowNormalizations(self):
        face = rubiksCube.Face(0)
        self.assertEqual(
            face.row(2, (1, 0, 0)),
            face.col(2),
            'getter rowsToCols normalization not working'
        )
        self.assertEqual(
            face.row(2, (0, 1, 0)),
            face.row(0),
            'getter invertIndexes normalization not working'
        )
        self.assertEqual(
            face.row(0, (0, 1, 0)),
            face.row(2),
            'getter invertIndexes normalization not working'
        )
        self.assertEqual(
            face.row(0, (0, 0, 1)),
            face.row(0)[::-1],
            'getter reverseRows normalization not working'
        )

        new = [1, 2, 3]
        norms = [
            (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0),
            (1, 0, 1), (1, 1, 0), (1, 1, 1), (0, 0, 0)
        ]
        for norm in norms:
            face.setRow(0, new, norm)
            self.assertEqual(face.row(0, norm), new,
                str(norm) + ' normalization not working')

    def test_faceRotate(self):
        face = rubiksCube.Face(1)
        face.rotate()
        self.assertEqual(face.face,[
            [(1, 2, 0), (1, 1, 0), (1, 0, 0)],
            [(1, 2, 1), (1, 1, 1), (1, 0, 1)],
            [(1, 2, 2), (1, 1, 2), (1, 0, 2)]
        ], 'face not rotating')
        face.rotate(False)
        self.assertEqual(face.face,[
            [(1, 0, 0), (1, 0, 1), (1, 0, 2)],
            [(1, 1, 0), (1, 1, 1), (1, 1, 2)],
            [(1, 2, 0), (1, 2, 1), (1, 2, 2)]
        ], 'face rotation is not symmetrical')

    def test_faceRepr(self):
        self.assertEqual(
            str(rubiksCube.Face(1)),
            '''[(1, 0, 0), (1, 0, 1), (1, 0, 2)],
[(1, 1, 0), (1, 1, 1), (1, 1, 2)],
[(1, 2, 0), (1, 2, 1), (1, 2, 2)]''',
            'face has wrong string representation'
        )


class TestCube(unittest.TestCase):

    def test_colorForTile(self):
        cube = rubiksCube.Cube()
        self.assertEqual(
            cube.colors[cube.SIDE_FRONT],
            cube.colorForTile(cube.front.tile(0, 0)),
            'tile color is not as expected'
        )

    def test_scrambleSolve(self):
        cube = rubiksCube.Cube()
        strRep = str(cube)
        cube.scramble(50)
        self.assertEqual(len(cube.pastMoves), 50,
            'scramble performed an incorrrect amount of moves')
        self.assertNotEqual(str(cube), strRep,
            'scramble did not change the cube')
        cube.solve()
        self.assertEqual(str(cube), strRep,
            'scramble/solve are not symmetric operations')

    def test_moveSymmetry(self):
        sides = [
            ('front', rubiksCube.Cube.SIDE_FRONT),
            ('back' , rubiksCube.Cube.SIDE_BACK ),
            ('up'   , rubiksCube.Cube.SIDE_UP   ),
            ('down' , rubiksCube.Cube.SIDE_DOWN ),
            ('left' , rubiksCube.Cube.SIDE_LEFT ),
            ('right', rubiksCube.Cube.SIDE_RIGHT)
        ]

        for n, f in sides:
            for i in range(10):
                cube = rubiksCube.Cube()
                cube.scramble(50)
                strRep = str(cube)

                cube.move(f, True)
                cube.move(f, False)

                self.assertEqual(strRep, str(cube),
                    n + ' movement is assymetric')
