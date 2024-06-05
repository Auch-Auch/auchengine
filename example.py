import pygame
from OpenGL.GL import *
from core.engine import PyEngineGL
from core.camera import Camera
from core.light import Light
from core.shader import Shader
from core.mesh import Axes, Mesh


class ExampleProgram(PyEngineGL):
    def __init__(self) -> None:
        super().__init__(0, 0, 1920, 1024)
        self.camera = None
        self.plane = None
        self.light = None
        self.shader = None
        glEnable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def initialize(self):
        self.shader = Shader(
            "shaders/textruedvert.vs",
            "shaders/texturedfrag.vs",
        )
        self.axes_mat = Shader(
            "shaders/vertexcolvert.vs",
            "shaders/vertexcolfrag.vs",
        )
        self.axes = Axes(self.axes_mat, pygame.Vector3(0, 0, 0))
        self.camera = Camera(self.screen_width, self.screen_height)
        self.light = Light(
            pygame.Vector3(5, 5, 5), color=pygame.Vector3(1, 1, 1), light_number=0
        )
        self.light2 = Light(
            pygame.Vector3(0, 0, 0), color=pygame.Vector3(1, 1, 1), light_number=1
        )
        self.plane = Mesh.load(
            "models/plane.obj",
            "images/crate.png",
            location=pygame.Vector3(0, 0, 0),
            shader=self.shader,
            scale=pygame.Vector3(2, 2, 2),
        )
        self.donut = Mesh.load(
            "models/donut.obj",
            shader=self.shader,
            location=pygame.Vector3(0, 0, 0),
            scale=pygame.Vector3(2, 2, 2),
        )
        glEnable(GL_DEPTH_TEST)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.shader.use()
        self.axes.draw(self.camera)
        self.donut.rotate(1, pygame.Vector3(1, 0, 1))
        self.donut.draw(self.camera, [self.light, self.light2])
        self.plane.draw(self.camera, [self.light])


if __name__ == "__main__":
    ExampleProgram().main_loop()
