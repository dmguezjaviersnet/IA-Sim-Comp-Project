import math
import pygame


class ElipticOrbit:
    def __init__(self, center, width, height):
        self.center = center
        self.size = (width, height)
        self.over_axis = 'x' if width > height else 'y'
        self.semi_major_axis = max(self.size)/2
        self.semi_minor_axis = min(self.size)/2
        self.focus = math.sqrt(self.semi_major_axis**2 - self.semi_minor_axis**2)
        if self.over_axis == 'x':
            self.vertex1 = (self.center[0] - self.semi_major_axis, self.center[1])
            self.vertex2 = (self.center[0] + self.semi_major_axis, self.center[1])
            self.covertex1 = (self.center[0], self.center[1] - self.semi_minor_axis)
            self.covertex2 = (self.center[0], self.center[1] + self.semi_minor_axis)
        else:
            self.vertex1 = (self.center[0], self.center[1] - self.semi_major_axis)
            self.vertex2 = (self.center[0], self.center[1] + self.semi_major_axis)
            self.covertex1 = (self.center[0] - self.semi_minor_axis, self.center[1])
            self.covertex2 = (self.center[0] + self.semi_minor_axis, self.center[1])
        self.rect = pygame.Rect(self.center[0]- width/2, self.center[1] - height/2, width, height)
        
    def __eq__(self, other: 'ElipticOrbit'):
        return self.semi_major_axis == other.semi_major_axis and self.semi_minor_axis == other.semi_minor_axis

    def draw_elipse(self, screen, color = (255,255,255)):
        pygame.draw.ellipse(screen, color,self.rect, 1)
        # pygame.draw.circle(screen, (255, 0, 0), self.vertex1, 4,0)
        # pygame.draw.circle(screen, (255, 0, 0), self.vertex2, 4,0)
        # pygame.draw.circle(screen, (255, 0, 0), self.covertex1, 4,0)
        # pygame.draw.circle(screen, (255, 0, 0), self.covertex2, 4,0)
        pygame.draw.circle(screen, (255, 255, 0), self.rect.topleft, 10,0)
      