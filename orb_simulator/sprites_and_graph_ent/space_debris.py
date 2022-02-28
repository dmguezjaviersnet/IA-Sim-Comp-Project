from urllib3 import Retry
from sprites_and_graph_ent.orbit_obj import OrbitObj
from tools import SOLID_BLUE_COLOR, GREEN_COLOR, SELECT_BLUE_COLOR, next_point_moving_in_elipse
import math
import pygame
import random
class SpaceDebris(OrbitObj):
    
    def __init__(self, pos_x, pos_y, a, b, orbit_center, vel: int = 0.5):
        super().__init__(a, b, orbit_center, vel)
        self.size = (random.randint(2,30),random.randint(2,30))
        self.image = pygame.Surface([self.size[0], self.size[1]])
        self.default_color = SOLID_BLUE_COLOR
        self.collision_color = GREEN_COLOR
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.image.set_colorkey((255, 0, 255))
        self.r = math.dist(self.rect.center, self.orbit_center)
        self.circular_speed = math.sqrt(self.G*self.earth_mass/self.r)
        self.circular_speed = 1 - 1/self.circular_speed
        self.id = id(self)
    
    @property
    def pos(self):
        return self.rect.center
    def __str__(self):
        return f'SpaceDebris {self.id} Size: {self.size} Position: {self.pos}'


    
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
    
    def draw_points(self, screen, color = (255, 255, 255)):
        pass
        # pygame.draw.circle(screen, (255, 255, 0), self.rect.topleft, 2,0)
        # pygame.draw.circle(screen, (255, 255, 0), self.rect.bottomright, 2,0)

    def draw_selection(self, surface):
        
        if self.selected:
            pygame.draw.line(surface,SELECT_BLUE_COLOR, self.orbit_center, self.rect.center,2)
            pygame.draw.rect(surface,SELECT_BLUE_COLOR, self.rect,2)
    
    def change_selected(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.selected = not self.selected

    def draw_collision(self, screen):
        self.image.fill(self.collision_color if self.is_colliding else self.default_color)
    
    