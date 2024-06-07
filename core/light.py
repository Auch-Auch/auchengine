import pygame
import core.transformations as transform
from core.uniform import UniformVec3


class Light:
    def __init__(self, position, color=pygame.Vector3(1, 1, 1), light_number=0):
        self.transformation = transform.identity_matrix()
        self.color = color
        self.position = position
        self.light_variable = "light_data[" + str(light_number) + "].position"
        self.color_variable = "light_data[" + str(light_number) + "].color"

    def update(self, program_id):
        light_pos = UniformVec3(self.position)
        light_pos.find_variable(program_id, self.light_variable)
        light_pos.load_data()
        color = UniformVec3(self.color)
        color.find_variable(program_id, self.color_variable)
        color.load_data()
