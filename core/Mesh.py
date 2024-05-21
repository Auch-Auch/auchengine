from OpenGL.GL import *
import pygame
import numpy as np
from core.GraphicsData import GraphicsData
from core.Uniform import Uniform
import core.Transformations as transform
from core.Texture import Texture


class Mesh:
    def __init__(
        self,
        vertices,
        imagefile=None,
        colors=None,
        draw_type=GL_TRIANGLES,
        vertex_normals=None,
        vertex_textures=None,
        translation=pygame.Vector3(0, 0, 0),
        rotation=transform.Rotation(0, pygame.Vector3(0, 1, 0)),
        scale=pygame.Vector3(1, 1, 1),
        material=None,
    ):
        self.material = material
        self.vertices = vertices
        self.colors = colors
        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1)
        self.vertex_normals = vertex_normals
        self.vetex_textures = vertex_textures
        self.image = None
        self.texture = None
        glBindVertexArray(self.vao_ref)
        position = GraphicsData("vec3", self.vertices)
        position.create_variable(self.material.program_id, "position")
        if colors is not None:
            colors = GraphicsData("vec3", self.colors)
            colors.create_variable(self.material.program_id, "vertex_color")
        if vertex_normals is not None:
            v_normals = GraphicsData("vec3", self.vertex_normals)
            v_normals.create_variable(self.material.program_id, "vertex_normal")
        self.transformation_mat = transform.rotateA(
            transform.identity_matrix(), rotation.angle, rotation.axis
        )
        self.transformation_mat = transform.translate(
            self.transformation_mat, translation.x, translation.y, translation.z
        )
        self.transformation_mat = transform.do_scale(
            self.transformation_mat, scale.x, scale.y, scale.z
        )
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.material.program_id, "model_mat")

        if imagefile is not None and vertex_textures is not None:
            textures = GraphicsData("vec2", self.vertex_textures)
            textures.create_variable(self.material.program_id, "vertex_uv")
            self.image = Texture(imagefile)
            self.texture = Uniform("sampler2D", [self.image.texture_id, 1])
            self.texture.find_variable(self.material.program_id, "tex")

    def rotate(self, angle, axis):
        self.transformation_mat = transform.rotateA(
            self.transformation_mat, angle, axis
        )
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.material.program_id, "model_mat")

    def translate(self, translation):
        self.transformation_mat = transform.translate(
            self.transformation_mat, translation.x, translation.y, translation.z
        )
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.material.program_id, "model_mat")

    def scale(self, scale):
        self.transformation_mat = transform.do_scale(
            self.transformation_mat, scale.x, scale.y, scale.z
        )
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.material.program_id, "model_mat")

    def draw(self, camera, lights=None):
        self.material.use()
        camera.update(self.material.program_id)
        if lights is not None:
            for light in lights:
                light.update(self.material.program_id)
        if self.texture:
            self.texture.load()
        self.transformation.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))


class Cube(Mesh):
    def __init__(self, program_id, location):
        self.vertices = np.array(
            [
                [-1, -1, 1],
                [1, -1, 1],
                [1, 1, 1],
                [1, 1, 1],
                [-1, 1, 1],
                [-1, -1, 1],
                # Back face
                [-1, -1, -1],
                [-1, 1, -1],
                [1, 1, -1],
                [1, 1, -1],
                [1, -1, -1],
                [-1, -1, -1],
                # Left face
                [-1, -1, -1],
                [-1, -1, 1],
                [-1, 1, 1],
                [-1, 1, 1],
                [-1, 1, -1],
                [-1, -1, -1],
                # Right face
                [1, -1, -1],
                [1, 1, -1],
                [1, 1, 1],
                [1, 1, 1],
                [1, -1, 1],
                [1, -1, -1],
                # Top face
                [-1, 1, -1],
                [-1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, -1],
                [-1, 1, -1],
                # Bottom face
                [-1, -1, -1],
                [1, -1, -1],
                [1, -1, 1],
                [1, -1, 1],
                [-1, -1, 1],
                [-1, -1, -1],
            ],
            dtype=np.float32,
        )

        colors = np.random.uniform(
            low=0.0, high=1.0, size=(len(self.vertices), 3)
        ).astype(np.float32)
        super().__init__(program_id, self.vertices, colors, GL_TRIANGLES, location)


class Axes(Mesh):
    def __init__(self, material, location):
        vertices = np.array(
            [
                [-100, 0.0, 0.0],
                [100, 0.0, 0.0],
                [0.0, -100, 0.0],
                [0.0, 100, 0.0],
                [0.0, 0.0, 100],
                [0.0, 0.0, -100],
            ],
            dtype=np.float32,
        )
        colors = np.array(
            [
                [1.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float32,
        )
        super().__init__(
            vertices,
            colors=colors,
            material=material,
            draw_type=GL_LINES,
            translation=location,
        )
