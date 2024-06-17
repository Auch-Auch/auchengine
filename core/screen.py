import os
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from core.camera import Camera
from core.mesh import Mesh


class Screen:  # TODO: define base class when interface is clear
    def __init__(
        self,
        screen_pos_x: int,
        screen_pos_y: int,
        screen_width: int,
        screen_height: int,
        camera: Camera,
    ) -> None:
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (screen_pos_x, screen_pos_y)
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height), DOUBLEBUF | OPENGL
        )
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )
        pygame.display.set_caption("PyEngineGL")
        glEnable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.objects: list[Mesh] = []
        self.camera = camera

    def add_object(self, object: Mesh) -> None:
        self.objects.append(object)

    def clear(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def display_objects(self) -> None:
        self.clear()
        for object in self.objects:
            object.draw(self.camera)
