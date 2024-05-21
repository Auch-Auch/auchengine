from OpenGL.GL import *
import pygame
import numpy as np
from core.Mesh import Mesh
import core.Transformations as transform


class LoadMesh(Mesh):

    def __init__(
        self,
        filename,
        imagefile=None,
        draw_type=GL_TRIANGLES,
        material=None,
        location=pygame.Vector3(0, 0, 0),
        rotation=transform.Rotation(0, pygame.Vector3(0, 1, 0)),
        scale=pygame.Vector3(1, 1, 1),
        colors=None,
    ):
        self.material = material
        self.coordinates = []
        self.triangles = []
        self.filename = filename
        self.normals = []
        self.textures = []
        self.normals_ids = []
        self.textures_ids = []
        self.draw_type = draw_type
        self.load_drawing(filename)
        self.vertices = self.form_vertices(self.coordinates, self.triangles)
        self.vertex_normals = self.form_vertices(self.normals, self.normals_ids)
        self.vertex_textures = self.form_vertices(self.textures, self.textures_ids)
        self.colors = (
            colors
            if colors is not None
            else np.random.uniform(0, 1, (len(self.vertices), 4)).astype(np.float32)
        )
        super().__init__(
            self.vertices,
            imagefile=imagefile,
            colors=self.colors,
            draw_type=self.draw_type,
            vertex_normals=self.vertex_normals,
            vertex_textures=self.vertex_textures,
            translation=location,
            rotation=rotation,
            scale=scale,
            material=material,
        )

    def form_vertices(self, coordinates, triangles):
        allTriangles = []
        for t in range(0, len(triangles), 3):
            allTriangles.extend(
                [
                    coordinates[triangles[t]],
                    coordinates[triangles[t + 1]],
                    coordinates[triangles[t + 2]],
                ]
            )
        return np.array(allTriangles, np.float32)

    def load_drawing(self, filename):
        with open(filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    self.coordinates.append((vx, vy, vz))
                if line[:2] == "vn":
                    nx, ny, nz = [float(value) for value in line[3:].split()]
                    self.normals.append((nx, ny, nz))
                if line[:2] == "vt":
                    tx, ty = [float(value) for value in line[3:].split()]
                    self.textures.append((tx, ty))
                if line[:2] == "f ":
                    t1, t2, t3 = [value for value in line[2:].split()]
                    self.triangles.append(
                        [int(value) for value in t1.split("/")][0] - 1
                    )
                    self.triangles.append(
                        [int(value) for value in t2.split("/")][0] - 1
                    )
                    self.triangles.append(
                        [int(value) for value in t3.split("/")][0] - 1
                    )
                    self.textures_ids.append(
                        [int(value) for value in t1.split("/")][1] - 1
                    )
                    self.textures_ids.append(
                        [int(value) for value in t2.split("/")][1] - 1
                    )
                    self.textures_ids.append(
                        [int(value) for value in t3.split("/")][1] - 1
                    )
                    self.normals_ids.append(
                        [int(value) for value in t1.split("/")][2] - 1
                    )
                    self.normals_ids.append(
                        [int(value) for value in t2.split("/")][2] - 1
                    )
                    self.normals_ids.append(
                        [int(value) for value in t3.split("/")][2] - 1
                    )

                line = fp.readline()
