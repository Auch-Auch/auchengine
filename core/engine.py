from abc import ABC, abstractmethod
import os
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *


class PyEngineGL(ABC):
    def __init__(self, screenPosX, screenPosY, screenWidth, screenHeight) -> None:
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (screenPosX, screenPosY)
        self.screen_width = screenWidth
        self.screen_height = screenHeight
        pygame.init()
        self.screen = pygame.display.set_mode(
            (screenWidth, screenHeight), DOUBLEBUF | OPENGL
        )
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )
        pygame.display.set_caption("PyEngineGL")
        self.camera = None
        self.clock = pygame.time.Clock()

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def display(self) -> None:
        pass

    def main_loop(self):
        done = False
        self.initialize()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    pygame.event.set_grab(False)
                    pygame.mouse.set_visible(True)
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    done = True
                    pygame.event.set_grab(False)
                    pygame.mouse.set_visible(True)
            self.display()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
