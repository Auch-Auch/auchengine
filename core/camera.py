import math
import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import core.transformations as transform
from core.uniform import Uniform


class Camera:
    def __init__(self, w, h):
        self.transfromation = transform.identity_matrix()
        self.last_mouse = pygame.math.Vector2(0, 0)
        self.mouse_sensativity = 0.2
        self.projection_mat = self.perspective_matrix(w / h, 60, 0.01, 10000)
        self.projection = Uniform("mat4", self.projection_mat)
        self.screen_width = w
        self.screen_height = h

    def rotate(self, yaw, pitch):
        forward = pygame.math.Vector3(
            self.transfromation[0][2],
            self.transfromation[1][2],
            self.transfromation[2][2],
        )
        up = pygame.Vector3(0, 1, 0)
        angle = forward.angle_to(up)
        self.transfromation = transform.rotate(
            self.transfromation, yaw, "y", local=False
        )
        if angle < 170.0 and pitch > 0 or angle > 30.0 and pitch < 0:
            self.transfromation = transform.rotate(
                self.transfromation, pitch, "x", local=True
            )

    def perspective_matrix(self, aspect, fov, zNear, zFar):
        a = math.radians(fov)
        d = 1.0 / math.tan(a / 2.0)
        r = aspect
        b = (zNear + zFar) / (zNear - zFar)
        c = zFar * zNear / (zNear - zFar)
        return np.array(
            [[d / r, 0, 0, 0], [0, d, 0, 0], [0, 0, b, c], [0, 0, -1, 0]],
            dtype=np.float32,
        )

    def update(self, program_id):
        if pygame.mouse.get_visible():
            return
        pygame.mouse.set_visible(False)
        mouse_pos = pygame.mouse.get_pos()
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        pygame.mouse.set_pos(self.screen_width / 2, self.screen_height / 2)
        self.last_mouse = pygame.mouse.get_pos()
        self.rotate(
            -mouse_change.x * self.mouse_sensativity,
            -mouse_change.y * self.mouse_sensativity,
        )

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.transfromation = transform.translate(
                self.transfromation, 0, 0, self.mouse_sensativity, local=True
            )
        if keys[pygame.K_UP]:
            self.transfromation = transform.translate(
                self.transfromation, 0, 0, -self.mouse_sensativity, local=True
            )

        if keys[pygame.K_RIGHT]:
            self.transfromation = transform.translate(
                self.transfromation, self.mouse_sensativity, 0, 0, local=True
            )
        if keys[pygame.K_LEFT]:
            self.transfromation = transform.translate(
                self.transfromation, -self.mouse_sensativity, 0, 0, local=True
            )

        self.projection.find_variable(program_id, "projection_mat")
        self.projection.load()
        lookat_mat = self.transfromation
        lookat = Uniform("mat4", lookat_mat)
        lookat.find_variable(program_id, "view_mat")
        lookat.load()
