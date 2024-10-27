from enum import Enum
from uuid import uuid4, UUID

import pygame

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)
def Cube():
    glPointSize(50)
    glBegin(GL_POINTS)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


class KeyEvent(Enum):
    KEY_DOWN = 1  # Every tick of key down
    KEY_UP = 2  # Every tick of key up
    KEY_PRESSED = 3  # Only once when key is pressed
    KEY_RELEASED = 4  # Only once when key is released


class Key:
    _key: int
    _pressed: bool
    _callbacks: dict[KeyEvent, dict[UUID, callable]]

    def __init__(self, key):
        self._key = key
        self._pressed = False
        self._callbacks = {event: {} for event in KeyEvent}

    def set_key_pressed(self, pressed: bool):
        if self._pressed and not pressed:
            for callback in self._callbacks[KeyEvent.KEY_RELEASED].values():
                callback()
        elif not self._pressed and pressed:
            for callback in self._callbacks[KeyEvent.KEY_PRESSED].values():
                callback()

        self._pressed = pressed

    def add_callback(self, event: KeyEvent, callback: callable) -> UUID:
        while (uid := uuid4()) in self._callbacks[event]:
            pass

        self._callbacks[event][uid] = callback
        return uid

    def remove_callback(self, event: KeyEvent, uid: UUID):
        if self._callbacks[event].get(uid):
            del self._callbacks[event][uid]

    def update(self):
        if self._pressed:
            for callback in self._callbacks[KeyEvent.KEY_DOWN].values():
                callback()
        else:
            for callback in self._callbacks[KeyEvent.KEY_UP].values():
                callback()


class KeyManager:
    keys: dict[int, Key]

    def __init__(self):
        self.keys = {}

    def get_key(self, key: int) -> Key:
        key_obj = self.keys.get(key)
        if not key_obj:
            key_obj = Key(key)
            self.keys[key] = key_obj

        return key_obj

    def update(self):
        for key in self.keys.values():
            key.update()

    def update_state(self, event: pygame.event.Event):
        key = self.get_key(event.key)
        key.set_key_pressed(event.type == pygame.KEYDOWN)

    def add_callback(self, key: int, event: KeyEvent, callback: callable) -> UUID:
        return self.get_key(key).add_callback(event, callback)

    def remove_callback(self, key: int, event: KeyEvent, uid: UUID):
        self.get_key(key).remove_callback(event, uid)


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    keys_manager = KeyManager()
    keys_manager.add_callback(K_ESCAPE, KeyEvent.KEY_RELEASED, lambda: pygame.quit())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys_manager.update_state(event)

        keys_manager.update()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

main()