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


def init_camera(fov: float, aspect: float, near: float, far: float):
    gluPerspective(fov, aspect, near, far)  # Perspective camera
    glTranslatef(0.0, 0.0, -5)  # Move back to see objects


def run():
    pygame.init()
    display = (1000, 1000)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    init_camera(45, display[0] / display[1], 0.1, 50.0)

    # KeyManager controls callbacks for specific key events
    keys_manager = KeyManager()
    keys_manager.add_callback(K_ESCAPE, KeyEvent.KEY_RELEASED, lambda: pygame.quit())

    tree = OctTree((0, 0, 0), (1, 1, 1), 1)
    particles = [Particle((random(), random(), random())) for _ in range(0, 1000)]

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
        for particle in particles:
            particle.draw()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    run()
