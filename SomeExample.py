import pygame
from OpenGL.GL import *
from core.PyEngine import PyEngineGL
from core.Camera import Camera
from core.LoadMesh import LoadMesh
from core.Light import Light
from core.Material import Material
from core.Mesh import Axes


class ExampleProgram(PyEngineGL):
    def __init__(self) -> None:
        super().__init__(0, 0, 1920, 1024)
        self.camera = None
        self.plane = None
        self.light = None
        self.material = None
        glEnable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def initialize(self):
        self.material = Material(
            "/home/aleksandr/game-engine/Engine3/shaders/textruedvert.vs",
            "/home/aleksandr/game-engine/Engine3/shaders/texturedfrag.vs",
        )
        self.axes_mat = Material(
            "/home/aleksandr/game-engine/Engine3/shaders/vertexcolvert.vs",
            "/home/aleksandr/game-engine/Engine3/shaders/vertexcolfrag.vs",
        )
        self.axes = Axes(self.axes_mat, pygame.Vector3(0, 0, 0))
        self.camera = Camera(self.screen_width, self.screen_height)
        self.light = Light(
            pygame.Vector3(5, 5, 5), color=pygame.Vector3(1, 1, 1), light_number=0
        )
        self.light2 = Light(
            pygame.Vector3(0, 0, 0), color=pygame.Vector3(1, 1, 1), light_number=1
        )
        self.plane = LoadMesh(
            "/home/aleksandr/game-engine/Engine2/models/plane.obj",
            "/home/aleksandr/game-engine/Engine2/models/crate.png",
            location=pygame.Vector3(0, 0, 0),
            material=self.material,
            scale=pygame.Vector3(2, 2, 2),
        )
        self.donut = LoadMesh(
            "/home/aleksandr/game-engine/Engine2/models/donut.obj",
            material=self.material,
            location=pygame.Vector3(0, 0, 0),
            scale=pygame.Vector3(2, 2, 2),
        )
        glEnable(GL_DEPTH_TEST)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.material.use()
        self.axes.draw(self.camera)
        self.donut.rotate(1, pygame.Vector3(1, 0, 1))
        self.donut.draw(self.camera, [self.light, self.light2])
        self.plane.draw(self.camera, [self.light])


ExampleProgram().main_loop()
