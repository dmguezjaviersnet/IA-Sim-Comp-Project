import pygame

class Sphere(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        rot_angle = 0
        while rot_angle < 360:
            self.sprites.append(pygame.image.load(f'./images/earth/img_rotate_{rot_angle}_grades.png').convert())
            rot_angle += 15
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect =  self.image.get_rect()
        # print(self.rect)
        self.rect.topleft =  [pos_x, pos_y]
        self.rot_a = 0 
        self.rot_s = float(1.5) 
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.index = 1

    def update(self):
        if self.is_animating:
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0 
            self.image = self.sprites[int(self.current_sprite)]
    
    def animate(self):
        self.is_animating = True
    
    def not_animate(self):
        self.is_animating = False
    