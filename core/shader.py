from dataclasses import dataclass
from OpenGL.GL import *
from typing import Self
import core.utils as utils


class Shader:  # TODO: looks like dataclass, refactor
    def __init__(
        self,
        vertex_shader: str,
        fragment_shader: str,
        vertex_position_var: str,
        vertex_color_var: str,
        model_matrix_var: str,
        projection_matrix_var: str,
        view_matrix_var: str,
        vertex_tex_var: str | None = None,
        vertex_tex_uv_var: str | None = None,
        vertex_normal_Var: str | None = None,
    ):
        self.vertex_position_var = vertex_position_var
        self.vertex_color_var = vertex_color_var
        self.model_matrix_var = model_matrix_var
        self.projection_matrix_var = projection_matrix_var
        self.view_matrix_var = view_matrix_var
        self.vertex_tex_var = vertex_tex_var
        self.vertex_tex_uv_var = vertex_tex_uv_var
        self.vertex_normal_Var = vertex_normal_Var
        self.program_id = utils.create_program(vertex_shader, fragment_shader)

    @classmethod
    def from_file(
        cls,
        vertex_shader_path: str,
        fragment_shader_path: str,
        vertex_position_var: str,
        vertex_color_var: str,
        model_matrix_var: str,
        projection_matrix_var: str,
        view_matrix_var: str,
        vertex_tex_var: str | None = None,
        vertex_tex_uv_var: str | None = None,
        vertex_normal_Var: str | None = None,
    ) -> Self:
        vertex_shader_program = utils.read_file(vertex_shader_path)
        fragment_shader_program = utils.read_file(fragment_shader_path)
        return cls(
            vertex_shader_program,
            fragment_shader_program,
            vertex_position_var,
            vertex_color_var,
            model_matrix_var,
            projection_matrix_var,
            view_matrix_var,
            vertex_tex_var,
            vertex_tex_uv_var,
            vertex_normal_Var,
        )

    def use(self):
        glUseProgram(self.program_id)
