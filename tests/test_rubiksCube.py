# Run like this: python -m unittest discover tests -v

import unittest, rubiksCube, copy

class TestFace(unittest.TestCase):

    def test_faceInit(self):
        self.assertEqual(rubiksCube.Face(1).face,[
            [(1, 0, 0), (1, 0, 1), (1, 0, 2)],
            [(1, 1, 0), (1, 1, 1), (1, 1, 2)],
            [(1, 2, 0), (1, 2, 1), (1, 2, 2)]
        ], 'face #1 incorrectly initialized')
        self.assertEqual(rubiksCube.Face(4).face,[
            [(4, 0, 0), (4, 0, 1), (4, 0, 2)],
            [(4, 1, 0), (4, 1, 1), (4, 1, 2)],
            [(4, 2, 0), (4, 2, 1), (4, 2, 2)]
        ], 'face #4 incorrectly initialized')
        self.assertEqual(rubiksCube.Face(0, 2).face,[
            [(0, 0, 0), (0, 0, 1)],
            [(0, 1, 0), (0, 1, 1)]
        ], 'size 2 face incorrectly initialized')


    def test_faceColRow(self):
        for size in [3, 2]:
            ssize = str(size)
            face = rubiksCube.Face(0, size)
            self.assertEqual(
                face.row(1),
                [(0, 1, 0), (0, 1, 1), (0, 1, 2)][:size],
                'face.row returned unexpected value with size ' + ssize
            )
            self.assertEqual(
                face.col(1),
                [(0, 0, 1), (0, 1, 1), (0, 2, 1)][:size],
                'face.col returned unexpected value with size ' + ssize
            )
            new = [0, 1, 2][:size]
            face.setRow(0, new)
            self.assertEqual(new, face.row(0),
                'face.setRow did not work properly with size ' + ssize)
            face.setCol(0, new)
            self.assertEqual(new, face.col(0),
                'face.setCol did not work properly with size ' + ssize)


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
        ], 'face not rotating with size 3')
        face.rotate(False)
        self.assertEqual(face.face,[
            [(1, 0, 0), (1, 0, 1), (1, 0, 2)],
            [(1, 1, 0), (1, 1, 1), (1, 1, 2)],
            [(1, 2, 0), (1, 2, 1), (1, 2, 2)]
        ], 'face rotation is not symmetrical with size 3')

        face = rubiksCube.Face(1, 2)
        face.rotate()
        self.assertEqual(face.face,[
            [(1, 1, 0), (1, 0, 0)],
            [(1, 1, 1), (1, 0, 1)]
        ], 'face not rotating with size 2')
        face.rotate(False)
        self.assertEqual(face.face,[
            [(1, 0, 0), (1, 0, 1)],
            [(1, 1, 0), (1, 1, 1)]
        ], 'face rotation is not symmetrical with size 2')

    def test_faceRepr(self):
        self.assertEqual(
            str(rubiksCube.Face(1)),
            '''[(1, 0, 0), (1, 0, 1), (1, 0, 2)],
[(1, 1, 0), (1, 1, 1), (1, 1, 2)],
[(1, 2, 0), (1, 2, 1), (1, 2, 2)]''',
            'face has wrong string representation with size 3'
        )

        self.assertEqual(
            str(rubiksCube.Face(1, 2)),
            '[(1, 0, 0), (1, 0, 1)],\n[(1, 1, 0), (1, 1, 1)]',
            'face has wrong string representation with size 2'
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
        for size in [2, 3]:
            ssize = str(size)
            cube = rubiksCube.Cube(size)
            strRep = str(cube)
            cube.scramble(50)
            self.assertEqual(len(cube.pastMoves), 50,
                'scramble performed wrong amount of moves with size ' + ssize)
            self.assertNotEqual(str(cube), strRep,
                'scramble did not change the cube with size ' + ssize)
            cube.solve()
            self.assertEqual(str(cube), strRep,
                'scramble/solve are asymmetric with size ' + ssize)

    def test_moveSymmetry(self):
        sides = [
            ('front', rubiksCube.Cube.SIDE_FRONT),
            ('back' , rubiksCube.Cube.SIDE_BACK ),
            ('up'   , rubiksCube.Cube.SIDE_UP   ),
            ('down' , rubiksCube.Cube.SIDE_DOWN ),
            ('left' , rubiksCube.Cube.SIDE_LEFT ),
            ('right', rubiksCube.Cube.SIDE_RIGHT)
        ]

        for size in [2, 3]:
            for n, f in sides:
                for i in range(10):
                    cube = rubiksCube.Cube(size)
                    cube.scramble(50)
                    strRep = str(cube)

                    cube.move(f, True)
                    cube.move(f, False)

                    self.assertEqual(strRep, str(cube),
                        n + ' movement is assymetric with size ' + str(size))
