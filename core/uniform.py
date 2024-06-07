from numbers import Number
from typing import Iterable, Protocol
from numpy.typing import NDArray
import numpy as np
from OpenGL.GL import *


def find_uniform_variable(program_id: int, variable_name: str) -> int:
    result = glGetUniformLocation(program_id, variable_name)
    if result == -1:
        raise Exception(f"Variable {variable_name} not found")
    return result


class Uniform(Protocol):
    data: NDArray[np.float32]
    variable_id: int | None = None

    def __init__(self, data: Iterable[Number] | NDArray) -> None:
        pass

    def find_variable(self, program_id: int, variable_name: str) -> int:
        pass

    def load_data(self) -> None:
        pass


class UniformSampler2D:
    def __init__(self, data: Iterable[Number] | NDArray):
        self.data = np.array(data, dtype=np.int32)
        self.variable_id = None
    
    def find_variable(self, program_id: int, variable_name: str) -> int:
        self.variable_id = find_uniform_variable(program_id, variable_name)

    def load_data(self):
        glActiveTexture(GL_TEXTURE0 + self.data[1])
        glBindTexture(GL_TEXTURE_2D, self.data[0])
        glUniform1i(self.variable_id, self.data[1])


class UniformVec3:
    def __init__(self, data: Iterable[Number] | NDArray):
        self.data = np.array(data, dtype=np.float32)
        self.variable_id = None
    
    def find_variable(self, program_id: int, variable_name: str) -> int:
        self.variable_id = find_uniform_variable(program_id, variable_name)

    def load_data(self):
        glUniform3f(self.variable_id, *self.data)


class UniformMat4:
    def __init__(self, data: Iterable[Number] | NDArray):
        self.data = data
        if isinstance(data, Iterable):
            self.data = np.array(data, dtype=np.float32).reshape((4, 4))
        self.variable_id = None
    
    def find_variable(self, program_id: int, variable_name: str) -> int:
        self.variable_id = find_uniform_variable(program_id, variable_name)

    def load_data(self):
        glUniformMatrix4fv(self.variable_id, 1, GL_TRUE, self.data)
