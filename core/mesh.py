from OpenGL.GL import *
import pygame
import numpy as np
from core.graphics_data import GraphicsData
from core.uniform import Uniform
import core.transformations as transform
from core.texture import Texture


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
        shader=None,
    ):
        self.shader = shader
        self.vertices = vertices
        self.colors = colors
        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1)
        self.vertex_normals = vertex_normals
        self.vertex_textures = vertex_textures
        self.image = None
        self.texture = None
        glBindVertexArray(self.vao_ref)
        position = GraphicsData("vec3", self.vertices)
        position.create_variable(self.shader.program_id, "position")
        if colors is not None:
            colors = GraphicsData("vec3", self.colors)
            colors.create_variable(self.shader.program_id, "vertex_color")
        if vertex_normals is not None:
            v_normals = GraphicsData("vec3", self.vertex_normals)
            v_normals.create_variable(self.shader.program_id, "vertex_normal")
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
        self.transformation.find_variable(self.shader.program_id, "model_mat")

        if imagefile is not None and vertex_textures is not None:
            textures = GraphicsData("vec2", self.vertex_textures)
            textures.create_variable(self.shader.program_id, "vertex_uv")
            self.image = Texture(imagefile)
            self.texture = Uniform("sampler2D", [self.image.texture_id, 1])
            self.texture.find_variable(self.shader.program_id, "tex")

    @staticmethod
    def form_vertices(coordinates, triangles):
        allTriangles = []
        for t in range(0, len(triangles), 3):
            allTriangles.extend(
                [
                    coordinates[triangles[t]],
                    coordinates[triangles[t + 1]],
                    coordinates[triangles[t + 2]],
                ]
            )
        return np.array(allTriangles, np.float32)

    @classmethod
    def load(
        cls,
        filename,
        imagefile=None,
        colors=None,
        draw_type=GL_TRIANGLES,
        location=pygame.Vector3(0, 0, 0),
        rotation=transform.Rotation(0, pygame.Vector3(0, 1, 0)),
        scale=pygame.Vector3(1, 1, 1),
        shader=None,
    ):
        coordinates = []
        normals = []
        textures = []
        triangles = []
        textures_ids = []
        normals_ids = []
        with open(filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    coordinates.append((vx, vy, vz))
                if line[:2] == "vn":
                    nx, ny, nz = [float(value) for value in line[3:].split()]
                    normals.append((nx, ny, nz))
                if line[:2] == "vt":
                    tx, ty = [float(value) for value in line[3:].split()]
                    textures.append((tx, ty))
                if line[:2] == "f ":
                    t1, t2, t3 = [value for value in line[2:].split()]
                    values_t1 = [int(value) for value in t1.split("/")]
                    triangles.append(values_t1[0] - 1)
                    textures_ids.append(values_t1[1] - 1)
                    normals_ids.append(values_t1[2] - 1)
                    values_t2 = [int(value) for value in t2.split("/")]
                    triangles.append(values_t2[0] - 1)
                    textures_ids.append(values_t2[1] - 1)
                    normals_ids.append(values_t2[2] - 1)
                    values_t3 = [int(value) for value in t3.split("/")]
                    triangles.append(values_t3[0] - 1)
                    textures_ids.append(values_t3[1] - 1)
                    normals_ids.append(values_t3[2] - 1)
                line = fp.readline()
        vertices = cls.form_vertices(coordinates, triangles)
        vertex_normals = cls.form_vertices(normals, normals_ids)
        vertex_textures = cls.form_vertices(textures, textures_ids)
        colors = (
            colors
            if colors is not None
            else np.random.uniform(0, 1, (len(vertices), 4)).astype(np.float32)
        )
        return cls(
            vertices,
            imagefile=imagefile,
            colors=colors,
            draw_type=draw_type,
            vertex_normals=vertex_normals,
            vertex_textures=vertex_textures,
            translation=location,
            rotation=rotation,
            scale=scale,
            shader=shader,
        )

    def rotate(self, angle, axis):
        self.transformation_mat = transform.rotateA(
            self.transformation_mat, angle, axis
        )
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.shader.program_id, "model_mat")

    def translate(self, translation):
        self.transformation_mat = transform.translate(
            self.transformation_mat, translation.x, translation.y, translation.z
        )
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.shader.program_id, "model_mat")

    def scale(self, scale):
        self.transformation_mat = transform.do_scale(
            self.transformation_mat, scale.x, scale.y, scale.z
        )
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.shader.program_id, "model_mat")

    def draw(self, camera, lights=None):
        self.shader.use()
        camera.update(self.shader.program_id)
        if lights is not None:
            for light in lights:
                light.update(self.shader.program_id)
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
    def __init__(self, shader, location):
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
            shader=shader,
            draw_type=GL_LINES,
            translation=location,
        )
