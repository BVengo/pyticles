from abc import ABC, abstractmethod
from typing import Generic

from .types import Vector3f


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
