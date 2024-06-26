import io
from typing import Self, Callable
from OpenGL.GL import *
import pygame
from numpy.typing import NDArray
import numpy as np
from core.uniform import UniformSampler2D, UniformMat4
import core.transformations as transform
from core.texture import Texture
from core.graphics_data import GraphicsDataVec
from core.shader import Shader
from core.utils import parse_obj
from core.light import Light
from core.camera import Camera
from core.utils import form_vertices


class Mesh:
    def __init__(
        self,
        vertices: NDArray,
        teximage: pygame.Surface | None = None,
        colors: NDArray | None = None,
        draw_type: int = GL_TRIANGLES,
        vertex_normals: NDArray | None = None,
        vertex_textures: NDArray | None = None,
        translation: pygame.Vector3 | None = None,
        rotation: transform.Rotation | None = None,
        scale: pygame.Vector3 | None = None,
        shader: Shader | None = None,
        lights: list[Light] | None = None,
    ):
        self.shader = shader
        self.vertices = vertices
        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1)
        self.vertex_normals = vertex_normals
        self.vertex_textures = vertex_textures
        self.texture = None
        self.texture_var = None
        self.init_translation = translation
        self.init_rotation = rotation
        self.init_scale = scale
        self.lights = lights or []
        self.init_translation = translation or pygame.Vector3(0, 0, 0)
        self.init_rotation = rotation or transform.Rotation(0, pygame.Vector3(0, 1, 0))
        self.init_scale = scale or pygame.Vector3(1, 1, 1)
        self.actions: list[Callable] = []

        self.colors = (
            colors
            if colors is not None
            else np.random.uniform(0, 1, (len(vertices), 4)).astype(np.float32)
        )
        glBindVertexArray(self.vao_ref)

        position = GraphicsDataVec(self.vertices)
        position.find_variable(
            self.shader.program_id, self.shader.vertex_position_var
        )  # TODO: refactor hardcoded variable
        position.load_data()
        colors = GraphicsDataVec(self.colors)
        colors.find_variable(self.shader.program_id, self.shader.vertex_color_var)
        colors.load_data()
        if vertex_normals is not None:
            v_normals = GraphicsDataVec(self.vertex_normals)
            v_normals.find_variable(
                self.shader.program_id, self.shader.vertex_normal_Var
            )
            v_normals.load_data()
        self.transformation_mat = transform.rotateA(
            transform.identity_matrix(),
            self.init_rotation.angle,
            self.init_rotation.axis,
        )
        self.transformation_mat = transform.translate(
            self.transformation_mat,
            self.init_translation,
        )
        self.transformation_mat = transform.do_scale(
            self.transformation_mat, self.init_scale
        )
        self.transformation = UniformMat4(self.transformation_mat)
        self.transformation.find_variable(
            self.shader.program_id, self.shader.model_matrix_var
        )
        if teximage is not None and vertex_textures is not None:
            textures = GraphicsDataVec(self.vertex_textures)
            textures.find_variable(
                self.shader.program_id, self.shader.vertex_tex_uv_var
            )
            textures.load_data()
            self.texture = Texture(teximage)
            self.texture_var = UniformSampler2D([self.texture.texture_id, 1])
            self.texture_var.find_variable(
                self.shader.program_id, self.shader.vertex_tex_var
            )

    @classmethod
    def from_stream(
        cls,
        source: io.BytesIO,
        teximage: pygame.Surface | None = None,
        colors: NDArray | None = None,
        draw_type: int = GL_TRIANGLES,
        translation: pygame.Vector3 | None = None,
        rotation: transform.Rotation | None = None,
        scale: pygame.Vector3 | None = None,
        shader: Shader | None = None,
    ) -> Self:
        coordinates, normals, textures, triangles, textures_ids, normals_ids = (
            parse_obj(source)
        )
        vertices = form_vertices(coordinates, triangles)
        vertex_normals = form_vertices(normals, normals_ids)
        vertex_textures = form_vertices(textures, textures_ids)
        return cls(
            vertices,
            teximage=teximage,
            colors=colors,
            draw_type=draw_type,
            vertex_normals=vertex_normals,
            vertex_textures=vertex_textures,
            translation=translation,
            rotation=rotation,
            scale=scale,
            shader=shader,
        )

    @classmethod
    def from_file(
        cls,
        path,
        teximage: pygame.Surface | None = None,
        colors: NDArray | None = None,
        draw_type: int = GL_TRIANGLES,
        translation: pygame.Vector3 | None = None,
        rotation: transform.Rotation | None = None,
        scale: pygame.Vector3 | None = None,
        shader: Shader | None = None,
    ) -> Self:
        with open(path, "rb") as f:
            return cls.from_stream(
                f, teximage, colors, draw_type, translation, rotation, scale, shader
            )

    def add_lights(self, lights: list[Light]) -> None:
        self.lights.extend(lights)

    def rotate(self, rotation: transform.Rotation) -> None:
        def func() -> None:
            self.transformation_mat = transform.rotateA(
                self.transformation_mat,
                rotation.angle,
                rotation.axis,
            )
            self.transformation = UniformMat4(self.transformation_mat)
            self.transformation.find_variable(
                self.shader.program_id, self.shader.model_matrix_var
            )
            self.transformation.load_data()

        self.actions.append(func)

    def translate(self, translation: pygame.Vector3) -> None:
        def func() -> None:
            self.transformation_mat = transform.translate(
                self.transformation_mat, translation
            )
            self.transformation = UniformMat4(self.transformation_mat)
            self.transformation.load_data()

        self.actions.append(func)

    def scale(self, scale: pygame.Vector3) -> None:
        def func() -> None:
            self.transformation_mat = transform.do_scale(self.transformation_mat, scale)
            self.transformation = UniformMat4(self.transformation_mat)
            self.transformation.load_data()

        self.actions.append(func)

    def draw(self, camera: Camera) -> None:
        self.shader.use()
        camera.update(self.shader)
        for light in self.lights:
            light.update(self.shader.program_id)
        if self.texture_var:
            self.texture_var.load_data()
        for action in self.actions:
            action()
        self.transformation.load_data()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))


class Cube(Mesh):
    def __init__(
        self, shader: Shader, translation: pygame.Vector3 = pygame.Vector3(0, 0, 0)
    ):
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
        super().__init__(
            self.vertices,
            teximage=None,
            colors=colors,
            translation=translation,
            shader=shader,
        )


class Axes(Mesh):
    def __init__(
        self, shader: Shader, translation: pygame.Vector3 = pygame.Vector3(0, 0, 0)
    ):
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
            translation=translation,
        )
