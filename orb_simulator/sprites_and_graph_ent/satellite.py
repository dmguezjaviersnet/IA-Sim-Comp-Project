from sprites_and_graph_ent.orbit_obj import OrbitObj
import pygame
import random
from tools import SOLID_BLUE_COLOR, LIGHT_GRAY, GREEN_COLOR, next_point_moving_in_elipse
import math
class Satellite(OrbitObj):
    def __init__(self, pos_x, pos_y, a, b, orbit_center, vel: int = 0.5):
        super().__init__(a, b, orbit_center, vel)
        self.image = pygame.image.load('./images/satellite1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.size = (self.rect.width, self.rect.height)
        self.rect.center = [pos_x, pos_y]
        self.image.set_colorkey((255, 0, 255))
        self.r = math.dist(self.rect.center, self.orbit_center)
        self.circular_speed = math.sqrt(self.G*self.earth_mass/self.r)
        self.circular_speed = 1 - 1/self.circular_speed
        self.id = id(self)
        self.life_time = None
        self.mass = None

    @property
    def pos(self):
        return self.rect.center

    @property
    def pos_x(self):
        return self.rect.center[0]
    
    @property
    def pos_y(self):
        return self.rect.center[1]

    @property
    def area(self):
        return self.rect.width * self.rect.height

    def __str__(self):
        return f'Satellite {self.id} Size: {self.size} Position: {self.pos}'
        
    def draw_selection(self, surface):
        
        if self.selected:
            pygame.draw.line(surface,LIGHT_GRAY, self.orbit_center, self.rect.center,2)
            pygame.draw.rect(surface,LIGHT_GRAY, self.rect,2)
    
    
    def update(self) -> None:
        nex_pos = next_point_moving_in_elipse(self.orbit_center,self.a, self.b, int(self.orbit_angle))
        self.rect.center = [nex_pos[0], nex_pos[1]]
        self.r = math.dist(self.rect.center, self.orbit_center)
        self.circular_speed = self.orbit_vel - 1/self.r
        # print(self.r)
        
        if self.clockwise:
            self.orbit_angle += self.circular_speed
        else:
            self.orbit_angle -= self.circular_speed
        if self.orbit_angle > 360:
            self.orbit_angle = 0
    
    def change_selected(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.selected = not self.selected
    
    def draw_collision(self, surface):
        if self.is_colliding:
            pygame.draw.rect(surface,GREEN_COLOR, self.rect,2)
    