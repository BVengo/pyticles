from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, TypeVar
from uuid import uuid4, UUID

import pygame

from pygame.locals import DOUBLEBUF, OPENGL, K_ESCAPE

from OpenGL.GL import (
    glBegin,
    glEnd,
    glVertex3fv,
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_LINES,
    glRotatef,
    glTranslatef,
)
from OpenGL.GLU import gluPerspective


Vector3f = TypeVar("Vector3f", bound=tuple[float, float, float])


class IDrawable(Generic[Vector3f], ABC):
    @property
    @abstractmethod
    def pos(self) -> Vector3f:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass


class IUpdatable(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass


class GameObject(IDrawable, IUpdatable, ABC):
    pass


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


class OctTree(Cube):
    def __init__(self, pos: Vector3f, dim: Vector3f, depth: int):
        super().__init__(pos, dim)
        self.depth = depth
        self.children = []

    def add(self, obj):
        pass

    def remove(self, obj):
        pass


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


def init_camera(fov: float, aspect: float, near: float, far: float):
    gluPerspective(fov, aspect, near, far)  # Perspective camera
    glTranslatef(0.0, 0.0, -5)  # Move back to see objects


def main():
    pygame.init()
    display = (1000, 1000)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    init_camera(45, display[0] / display[1], 0.1, 50.0)

    # KeyManager controls callbacks for specific key events
    keys_manager = KeyManager()
    keys_manager.add_callback(K_ESCAPE, KeyEvent.KEY_RELEASED, lambda: pygame.quit())

    tree = OctTree((0, 0, 0), (1, 1, 1), 1)

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
    main()
