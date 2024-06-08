from numbers import Number
from typing import Protocol, Iterable
from OpenGL.GL import *
import numpy as np
from numpy.typing import NDArray


def load_vec(
    data: NDArray[np.float32],
    buffer_ref: int,
    variable_id: int,
) -> None:
    # TODO: Refactor to use a buffer/loader object?
    glBindBuffer(GL_ARRAY_BUFFER, buffer_ref)
    glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)
    glVertexAttribPointer(variable_id, data.shape[1], GL_FLOAT, False, 0, None)
    glEnableVertexAttribArray(variable_id)


class GraphicsData(Protocol):
    data: NDArray[np.float32]
    buffer_ref: int
    variable_id: int | None = None

    def __init__(self, data: Iterable[Number] | NDArray) -> None:
        pass

    def finad_variable(self, program_id: int, variable_name: str):
        pass

    def load_data(self) -> None:
        pass


class GraphicsDataVec:
    def __init__(self, data: Iterable[Number] | NDArray):
        self.data = np.array(data, dtype=np.float32)
        self.buffer_ref = glGenBuffers(1)
        self.variable_id = None

    def find_variable(self, program_id: int, variable_name: str):
        self.variable_id = glGetAttribLocation(program_id, variable_name)

    def load_data(self):
        load_vec(self.data, self.buffer_ref, self.variable_id)
