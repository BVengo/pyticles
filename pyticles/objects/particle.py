from OpenGL.GL import glBegin, glEnd, glVertex3fv, GL_POINTS
from OpenGL.raw.GL.VERSION.GL_1_0 import glPointSize, glEnable
from OpenGL.raw.GLES1.VERSION.GLES1_1_0 import GL_POINT_SMOOTH

from pyticles.interfaces import GameObject


PARTICLE_SIZE = 5


class Particle(GameObject):
    def __init__(self, pos):
        self._pos = pos

    def draw(self):
        glEnable(GL_POINT_SMOOTH)
        glPointSize(PARTICLE_SIZE)
        glBegin(GL_POINTS)
        glVertex3fv(self._pos)
        glEnd()

    def update(self, dt):
        pass

    @property
    def pos(self):
        return self._pos