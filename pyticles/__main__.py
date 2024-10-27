import pygame
from random import random

from pygame.locals import DOUBLEBUF, OPENGL, K_ESCAPE

from OpenGL.GL import (
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    glRotatef,
    glTranslatef,
)
from OpenGL.GLU import gluPerspective

from pyticles.input import KeyManager, KeyEvent
from pyticles.objects import OctTree, Particle


DISPLAY_SIZE = 1000, 1000
FOV = 45
NEAR = 0.1
FAR = 50.0

NUM_PARTICLES = 1000
DISPLAY_TREE = False

def init_camera(fov: float, aspect: float, near: float, far: float):
    gluPerspective(fov, aspect, near, far)  # Perspective camera
    glTranslatef(0.0, 0.0, -5)  # Move back to see objects


def run():
    pygame.init()
    pygame.display.set_mode(DISPLAY_SIZE, DOUBLEBUF | OPENGL)

    init_camera(FOV, DISPLAY_SIZE[0] / DISPLAY_SIZE[1], NEAR, FAR)

    # KeyManager controls callbacks for specific key events
    keys_manager = KeyManager()
    keys_manager.add_callback(K_ESCAPE, KeyEvent.KEY_RELEASED, lambda: pygame.quit())

    tree = OctTree((0, 0, 0), (1, 1, 1), 0)
    tree.enable_draw(DISPLAY_TREE)
    [tree.add(Particle((random(), random(), random()))) for _ in range(0, NUM_PARTICLES)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys_manager.update_state(event)

        keys_manager.update()

        if not pygame.display.get_init():
            break

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        tree.draw()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    run()
