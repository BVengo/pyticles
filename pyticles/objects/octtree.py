from pyticles.objects import Cube
from pyticles.types import Vector3f


class OctTree(Cube):
    def __init__(self, pos: Vector3f, dim: Vector3f, depth: int):
        super().__init__(pos, dim)
        self.depth = depth
        self.children = []

    def add(self, obj):
        pass

    def remove(self, obj):
        pass
