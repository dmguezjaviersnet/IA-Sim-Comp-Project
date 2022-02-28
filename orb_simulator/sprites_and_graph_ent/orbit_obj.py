from  sprites_and_graph_ent.space_obj import SpaceObj
import pygame
import random
import math

class OrbitObj(SpaceObj):

    def __init__(self, a, b, orbit_center, vel: int = 0.5):
        super().__init__()
        self.is_colliding = False
        self.orbit_angle = 0
        self.orbit_vel = vel
        self.a = a 
        self.b = b
        self.orbit_center = orbit_center
        self.G = 67
        self.earth_mass = 9.8
        self.clockwise = random.randint(0,1)
        self.selected =  False
    
    def update(self) -> None:...
    def draw_selection(self, surface):...
    def change_selected(self):...
    def draw_collision(self, screen):...
    