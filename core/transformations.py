import numpy as np


class Rotation:
    def __init__(self, angle, axis):
        self.angle = angle
        self.axis = axis


def identity_matrix():
    return np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        np.float32,
    )


def translate_matrix(x, y, z):
    return np.array(
        [
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1],
        ],
        np.float32,
    )


def scale_matrix(x, y, z):
    return np.array(
        [
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1],
        ],
        np.float32,
    )


def rotate_x_mat(angle):
    c = np.cos(np.radians(angle))
    s = np.sin(np.radians(angle))
    return np.array(
        [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]], np.float32
    )


def rotate_y_mat(angle):
    c = np.cos(np.radians(angle))
    s = np.sin(np.radians(angle))
    return np.array(
        [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]], np.float32
    )


def rotate_z_mat(angle):
    c = np.cos(np.radians(angle))
    s = np.sin(np.radians(angle))
    return np.array(
        [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32
    )


def rotate_axis_matrix(theta, axis):
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


def translate(matrix, x, y, z, local=False):
    if local:
        return matrix @ translate_matrix(x, y, z)
    return translate_matrix(x, y, z) @ matrix


def do_scale(matrix, x, y, z):
    return matrix @ scale_matrix(x, y, z)


def rotate(matrix, angle, axis, local=True):
    rot = identity_matrix()
    if axis == "x":
        rot = rotate_x_mat(angle)
    if axis == "y":
        rot = rotate_y_mat(angle)
    if axis == "z":
        rot = rotate_z_mat(angle)
    if local:
        return matrix @ rot
    else:
        return rot @ matrix


def rotateA(matrix, theta, axis, local=True):
    """rotates about any axis"""
    if local:
        return matrix @ rotate_axis_matrix(theta, axis)
    return rotate_axis_matrix(theta, axis) @ matrix
