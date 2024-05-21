from OpenGL.GL import *
import core.Utils as utils


class Material:
    def __init__(self, vertex_shader, fragment_shader):
        vertex_shader_program = utils.read_file(vertex_shader)
        fragment_shader_program = utils.read_file(fragment_shader)
        self.program_id = utils.create_program(
            vertex_shader_program, fragment_shader_program
        )

    def use(self):
        glUseProgram(self.program_id)
