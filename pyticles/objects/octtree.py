from __future__ import annotations
from typing import Optional, Tuple

from OpenGL.GL import glBegin, glEnd, glVertex3fv, GL_LINES

from pyticles.interfaces import GameObject
from pyticles.objects import Cube
from pyticles.types import Vector3f


class OctTree(Cube):
    depth: int
    mid: Vector3f
    octants: Optional[Tuple[OctTree, OctTree, OctTree, OctTree, OctTree, OctTree, OctTree, OctTree]]
    child: Optional[GameObject]

    _should_draw: bool = False

    def __init__(self, pos: Vector3f, dim: Vector3f, depth: int = 0):
        super().__init__(pos, dim)
        self.octants = None
        self.child = None
        self.depth = depth
        self.mid = (pos[0] + dim[0] / 2, pos[1] + dim[1] / 2, pos[2] + dim[2] / 2)

    def get_octant(self, pos: Vector3f) -> OctTree:
        x, y, z = pos

        if x < self.mid[0]:
            if y < self.mid[1]:
                if z < self.mid[2]:
                    return self.octants[0]
                return self.octants[4] if z < self.mid[2] else self.octants[5]
            if z < self.mid[2]:
                return self.octants[2]
            return self.octants[6] if z < self.mid[2] else self.octants[7]
        if y < self.mid[1]:
            if z < self.mid[2]:
                return self.octants[1]
            return self.octants[5] if z < self.mid[2] else self.octants[4]
        if z < self.mid[2]:
            return self.octants[3]
        return self.octants[7] if z < self.mid[2] else self.octants[6]

    def _split(self):
        new_depth = self.depth + 1
        half_dim = (self.dim[0] / 2, self.dim[1] / 2, self.dim[2] / 2)
        cx, cy, cz = self.pos

        # Define each octant based on position offsets
        self.octants = (
            OctTree((cx, cy, cz), half_dim, new_depth),
            OctTree((self.mid[0], cy, cz), half_dim, new_depth),
            OctTree((cx, self.mid[1], cz), half_dim, new_depth),
            OctTree((self.mid[0], self.mid[1], cz), half_dim, new_depth),
            OctTree((cx, cy, self.mid[2]), half_dim, new_depth),
            OctTree((self.mid[0], cy, self.mid[2]), half_dim, new_depth),
            OctTree((cx, self.mid[1], self.mid[2]), half_dim, new_depth),
            OctTree(self.mid, half_dim, new_depth),
        )

        # Move existing child to the correct octant after splitting
        if self.child is not None:
            self.get_octant(self.child.pos).add(self.child)
            self.child = None

    def add(self, obj: GameObject):
        if self.octants is None:
            if self.child is None:
                # No child, add the object here
                self.child = obj
                return
            else:
                # Split, and add the existing child to the correct octant
                self._split()

        # Add the new object to the correct octant
        self.get_octant(obj.pos).add(obj)

    def remove(self, obj: GameObject):
        if self.octants is None:
            if self.child == obj:
                self.child = None
            return
        self.get_octant(obj.pos).remove(obj)

    def draw(self):
        if self._should_draw:
            super().draw()

        if self.octants is not None:
            for octant in self.octants:
                octant.draw()
        elif self.child is not None:
            self.child.draw()

    def enable_draw(self, should_draw: bool):
        self._should_draw = should_draw
        if self.octants is not None:
            for octant in self.octants:
                octant.enable_draw(should_draw)