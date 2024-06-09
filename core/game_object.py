from typing import Protocol
from core.mesh import Mesh
from core.camera import Camera
from core.light import Light


class BaseGameObject(Protocol):

    def display(self, camera: Camera) -> None:
        pass

    def add_light(self, light: Light) -> None:
        pass


class GameObject:
    def __init__(self, mesh: Mesh) -> None:
        self.mesh = mesh
        self.lights: list[Light] = []

    def add_light(self, light: Light) -> None:
        self.lights.append(light)

    def display(self, camera: Camera) -> None:
        self.mesh.draw(camera, self.lights)
