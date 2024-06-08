import pygame
import dataclasses
from numpy.typing import NDArray
import numpy as np


@dataclasses.dataclass(frozen=True, slots=True)
class Rotation:
    angle: float
    axis: pygame.Vector3


def identity_matrix() -> NDArray:
    return np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        np.float32,
    )


def translate_matrix(vec: pygame.Vector3) -> NDArray:
    return np.array(
        [
            [1, 0, 0, vec.x],
            [0, 1, 0, vec.y],
            [0, 0, 1, vec.z],
            [0, 0, 0, 1],
        ],
        np.float32,
    )


def scale_matrix(vec: pygame.Vector3) -> NDArray:
    return np.array(
        [
            [vec.x, 0, 0, 0],
            [0, vec.y, 0, 0],
            [0, 0, vec.z, 0],
            [0, 0, 0, 1],
        ],
        np.float32,
    )


def rotate_x_mat(angle: float) -> NDArray:
    c = np.cos(np.radians(angle))
    s = np.sin(np.radians(angle))
    return np.array(
        [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]], np.float32
    )


def rotate_y_mat(angle: float) -> NDArray:
    c = np.cos(np.radians(angle))
    s = np.sin(np.radians(angle))
    return np.array(
        [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]], np.float32
    )


def rotate_z_mat(angle: float) -> NDArray:
    c = np.cos(np.radians(angle))
    s = np.sin(np.radians(angle))
    return np.array(
        [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32
    )


def rotate_axis_matrix(theta: float, axis: pygame.Vector3) -> NDArray:
    """matrix that rotates about any axis"""
    c = np.cos(np.radians(theta))
    s = np.sin(np.radians(theta))
    axis = axis.normalize()
    ux2 = axis.x * axis.x
    uy2 = axis.y * axis.y
    uz2 = axis.z * axis.z
    return np.array(
        [
            [
                ux2 + (1 - ux2) * c,
                axis.x * axis.y * (1 - c) - axis.z * s,
                axis.x * axis.z * (1 - c) + axis.y * s,
                0,
            ],
            [
                axis.x * axis.y * (1 - c) + axis.z * s,
                uy2 + (1 - uy2) * c,
                axis.y * axis.z * (1 - c) - axis.x * s,
                0,
            ],
            [
                axis.x * axis.z * (1 - c) - axis.y * s,
                axis.y * axis.z * (1 - c) + axis.x * s,
                uz2 + (1 - uz2) * c,
                0,
            ],
            [0, 0, 0, 1],
        ],
        np.float32,
    )


def translate(matrix: NDArray, vec: pygame.Vector3, local: bool = False) -> NDArray:
    if local:
        return matrix @ translate_matrix(vec)
    return translate_matrix(vec) @ matrix


def do_scale(matrix: NDArray, vec: pygame.Vector3) -> NDArray:
    return matrix @ scale_matrix(vec)


def rotate(matrix: NDArray, angle: float, axis: str, local: bool = True):
    rot = identity_matrix()
    if axis == "x":
        rot = rotate_x_mat(angle)
    elif axis == "y":
        rot = rotate_y_mat(angle)
    elif axis == "z":
        rot = rotate_z_mat(angle)
    if local:
        return matrix @ rot
    else:
        return rot @ matrix


def rotateA(matrix: NDArray, theta: float, axis: pygame.Vector3, local: bool = True):
    """rotates about any axis"""
    if local:
        return matrix @ rotate_axis_matrix(theta, axis)
    return rotate_axis_matrix(theta, axis) @ matrix
