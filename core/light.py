import pygame
import core.transformations as transform
from core.uniform import UniformVec3


class Light:
    def __init__(self, position: pygame.Vector3, color: pygame.Vector3 | None = None, light_number: int = 0):
        if color is None:
            color = pygame.Vector3(1, 1, 1)
        self.transformation = transform.identity_matrix()
        self.color = color
        self.position = position
        self.light_variable = f"light_data[{str(light_number)}].position"
        self.color_variable = f"light_data[{str(light_number)}].color"
        self.light_pos = UniformVec3(self.position)
        self.color = color = UniformVec3(self.color)

    def update(self, program_id: int) -> None:
        self.light_pos.find_variable(program_id, self.light_variable)
        self.light_pos.load_data()
        self.color.find_variable(program_id, self.color_variable)
        self.color.load_data()
