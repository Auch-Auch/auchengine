from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pygame.locals import *


def compile_shaders(shader_type, shader_source):
    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, shader_source)
    glCompileShader(shader_id)
    result = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not result:
        error = glGetShaderInfoLog(shader_id)
        glDeleteShader(shader_id)
        error = "\n" + error.decode("utf-8")
        raise Exception(error)
    return shader_id


def create_program(vertex_shader_code, fragment_shader_code):
    vertex_shader_id = compile_shaders(GL_VERTEX_SHADER, vertex_shader_code)
    fragmet_shader_id = compile_shaders(GL_FRAGMENT_SHADER, fragment_shader_code)
    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragmet_shader_id)
    glLinkProgram(program_id)
    result = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not result:
        error = glGetProgramInfoLog(program_id)
        glDeleteProgram(program_id)
        error = "\n" + error.decode("utf-8")
        raise Exception(error)
    return program_id


def read_file(path) -> str:
    with open(path) as f:
        return f.read()
