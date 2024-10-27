from OpenGL.GL import glBegin, glVertex3fv, GL_LINES, glEnd

from pyticles.interfaces import GameObject
from pyticles.types import Vector3f


class Cube(GameObject):
    def __init__(self, pos: Vector3f, dim: Vector3f):
        self._pos = pos
        self.dim = dim

        self.vertices = [
            (x, y, z) for x in (0, dim[0]) for y in (0, dim[1]) for z in (0, dim[2])
        ]
        self.edges = (
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
        )

    def draw(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])

        glEnd()

    def update(self, dt: float):
        pass

    @property
    def pos(self) -> Vector3f:
        return self._pos
