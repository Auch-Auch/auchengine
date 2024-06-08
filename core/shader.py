from OpenGL.GL import *
from typing import Self
import core.utils as utils


class Shader:
    def __init__(self, vertex_shader: str, fragment_shader: str):
        self.program_id = utils.create_program(vertex_shader, fragment_shader)

    @classmethod
    def from_file(cls, vertex_shader_path: str, fragment_shader_path: str) -> Self:
        vertex_shader_program = utils.read_file(vertex_shader_path)
        fragment_shader_program = utils.read_file(fragment_shader_path)
        return cls(vertex_shader_program, fragment_shader_program)

    def use(self):
        glUseProgram(self.program_id)
