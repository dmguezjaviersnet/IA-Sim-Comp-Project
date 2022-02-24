import pygame
from tools import next_point_moving_in_elipse, BLUE

class Junk(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, type: str, a, b, orbit_center, vel: int = 0.5):
        super().__init__()
        path = ''
        if type == 'rock':
            path = './images/rock1.png'
        if type == 'satellite':
            path = './images/satellite1.png'
        self.type =  type
        self.image = pygame.Surface([5,5.5]) 
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

        self.image.set_colorkey(( 255,   0, 255))
        self.orbit_angle = 0
        self.orbit_vel = vel
        self.a = a 
        self.b = b
        self.orbit_center = orbit_center
        self.selected =  False
    
    def update(self) -> None:
        nex_pos = next_point_moving_in_elipse(self.orbit_center,self.a, self.b, int(self.orbit_angle))
        self.rect.center = [nex_pos[0], nex_pos[1]]
        self.orbit_angle += self.orbit_vel
        if self.orbit_angle > 360:
            self.orbit_angle = 0
    
    def draw_points(self, screen, color = (255,255,255)):
        pygame.draw.circle(screen, (255, 255, 0), self.rect.topleft, 2,0)
        pygame.draw.circle(screen, (255, 255, 0), self.rect.bottomright, 2,0)

    def draw_selection(self, surface):
        
        if self.selected:
            pygame.draw.line(surface,BLUE, self.orbit_center, self.rect.center,2)
            pygame.draw.rect(surface,BLUE, self.rect,2)
    
    def change_selected(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.selected = not self.selected