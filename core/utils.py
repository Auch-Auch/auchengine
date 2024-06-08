import io
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


def parse_obj(
    content: io.BytesIO,
) -> tuple[
    list[tuple[float, float, float]],
    list[tuple[float, float, float]],
    list[tuple[float, float]],
    list[int],
    list[int],
    list[int],
]:
    coordinates = []
    normals = []
    textures = []
    triangles = []
    textures_ids = []
    normals_ids = []

    while line := content.readline():
        if line.startswith(b"v "):
            _, vx, vy, vz = line.split(b" ")
            coordinates.append((float(vx), float(vy), float(vz)))
        elif line.startswith(b"vn"):
            _, nx, ny, nz = line.split(b" ")
            normals.append((float(nx), float(ny), float(nz)))
        elif line.startswith(b"vt"):
            _, tx, ty = line.split(b" ")
            textures.append((float(tx), float(ty)))
        elif line.startswith(b"f "):
            _, t1, t2, t3 = line.split(b" ")
            for t in [t1, t2, t3]:
                v, t, n = map(int, t.split(b"/"))
                triangles.append(v - 1)
                textures_ids.append(t - 1)
                normals_ids.append(n - 1)

    return coordinates, normals, textures, triangles, textures_ids, normals_ids
