import pygame
from OpenGL.GL import *
from core.camera import Camera
from core.light import Light
from core.shader import Shader
from core.mesh import Axes, Mesh
from core.transformations import Rotation
from core.screen import Screen
from core.game_loop import GameLoop
from core.camera import Camera


class SimpleExample:
    def __init__(self) -> None:
        self.camera = Camera(800, 600)
        self.screen = Screen(0, 0, 800, 600, self.camera)
        self.plane = None
        self.shader = None

    def initialize(self):
        self.shader = Shader.from_file(
            "shaders/textruedvert.vs",
            "shaders/texturedfrag.vs",
            "position",
            "vertex_color",
            "model_mat",
            "projection_mat",
            "view_mat",
            "tex",
            "vertex_uv",
            "vertex_normal",
        )
        self.axes_mat = Shader.from_file(
            "shaders/vertexcolvert.vs",
            "shaders/vertexcolfrag.vs",
            "position",
            "vertex_color",
            "model_mat",
            "projection_mat",
            "view_mat",
        )
        self.axes = Axes(self.axes_mat, pygame.Vector3(0, 0, 0))

        self.light = Light(
            pygame.Vector3(5, 5, 5), color=pygame.Vector3(1, 1, 1), light_number=0
        )
        self.light2 = Light(
            pygame.Vector3(0, 0, 0), color=pygame.Vector3(1, 1, 1), light_number=1
        )

        self.plane = Mesh.from_file(
            "models/plane.obj",
            pygame.image.load("images/crate.png"),
            translation=pygame.Vector3(0, 0, 0),
            shader=self.shader,
            scale=pygame.Vector3(2, 2, 2),
        )

        self.donut = Mesh.from_file(
            "models/donut.obj",
            shader=self.shader,
            translation=pygame.Vector3(0, 0, 0),
            scale=pygame.Vector3(2, 2, 2),
        )
        self.donut.add_lights([self.light, self.light2])
        self.donut.rotate(Rotation(0.5, pygame.Vector3(0.5, 1, 0.5)))
        self.screen.add_object(self.donut)
        self.screen.add_object(self.axes)
        self.screen.add_object(self.plane)

    def display(self):
        self.shader.use()
        self.screen.display_objects()


if __name__ == "__main__":
    game = SimpleExample()
    game.initialize()
    game_loop = GameLoop(60)
    game_loop.register_display_function(game.display)
    game_loop.run()
