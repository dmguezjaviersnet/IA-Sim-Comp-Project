from sprites_and_graph_ent.orbit_obj import OrbitObj
import pygame
import random
from tools import SOLID_BLUE_COLOR, LIGHT_GRAY
class Satellite(OrbitObj):
    def __init__(self, pos_x, pos_y, a, b, orbit_center, life_time: int, mass: int, vel: int = 0.5):
        super().__init__(pos_x, pos_y, a, b, orbit_center, vel)
        self.default_color = LIGHT_GRAY
        self.image.fill(self.default_color)
        self.life_time = life_time
        self.mass = mass

    @property
    def area(self):
        return self.rect.width * self.rect.height
       
    
    