
# Importing pygame module
from ctypes.wintypes import POINT
from dataclasses import dataclass
import random
from typing import List
import pygame
from pygame.locals import *
from pytest import Instance


# @dataclass
# class Point:
#     x: int
#     y: int
#     connected_points = []
    
#     @property
#     def degree(self):
#         return len(self.connected_points)
    
#     def __eq__(self, other:'Point') -> bool:
#         if isinstance(other, Point):
#             return other.x == self.x and other.y == self.y
#         return False
    
#     def __ne__(self, other: object) -> bool:
#         if isinstance(other, Point):
#             return not(other.x == self.x and other.y == self.y)
#         return True
#     def __hash__(self) -> int:
#         return hash((self.x,self.y))
    
#     def trace_line(self, other: 'Point'):
#         if other not in self.connected_points:
#             self.connected_points.append(other)
            
    

# def is_hamiltonian(points:List['Point']):
#     return len(points) >= 3 and all(i.degree >= 2 and i.degree %2 ==0 for i in points)
# def lines_generator(points: List['Point']):
    
#     for p_index, p in  enumerate(points):
#         p.trace_line(points[(p_index +1)%2])
#     # while not is_hamiltonian(points):
#     #     p1 = points[random.randint(0,len(points)-1)]
#     #     p2 = points[random.randint(0,len(points)-1)]
#     #     if not (p1 == p2):
#     #         p1.trace_line(p2)
    
# def verify_obs(points: List['Point'], point):
#     ...


# def points_generator(start_x: int, start_y: int):
#     points_set = set()
#     gui =0
#     for _ in range(4):
#         x = random.randint(start_x + gui,100 + start_x)
#         y = random.randint(start_y + gui,100 + start_y)
        
#         points_set.add(Point(x,y))
#         gui += 20
#     return list(points_set)
# # initiate pygame and give permission
# # to use pygame's functionality.
# # pygame.init()

    


# # points = points_generator()
# surface = pygame.display.set_mode((1000, 1000))
    
#     # Fill the scree with white color
# surface.fill((255, 255, 255))
# count = 0
# counters = set()
# while True:

#     for event in pygame.event.get() :
  
#         # if event object type is QUIT
#         # tpoints = points_generator()
# print(points, len(points))hen quitting the pygame
#         # and program both.
#         if event.type == pygame.QUIT :
  
#             # deactivates the pygame library
#             pygame.quit()
  
#             # quit the program.
#             quit()
  
#         # Draws the surface object to the screen.  
#     pygame.display.update() 
#     # create the display surface object
#     # of specific dimension.
    
    
#     # Using draw.rect module of
#     # pygame to draw the outlined rectangle
#     # pygame.draw.rect(surface, (0, 0, 255),
#     #                  [100, 100, 400, 100], 2)
    
#     # Draws the surface object to the screen.
#     # for point in points_generator():
  
    
#     if count < 1:
#         points =points_generator(random.randint(0,1000), random.randint(0,1000))
#         lines_generator(points)
#         for point in points:
#             for p in point.connected_points:
#                 if (point, p) or (p, point) not in counters:
#                     pygame.draw.line(surface, (10,2,3), [point.x,point.y],[p.x,p.y],2)
#                     counters.add((point, p))
#         pygame.display.update()
#         count +=1 
#     for i in range(2):

#         pygame.draw.circle(surface, (255, 0, 0),
#                        [40, 40], 40)

    

# import pygame, random, math

# red = (255, 0, 0)
# width = 800
# height = 600
# circle_num = 20
# tick = 2
# speed = 5

# pygame.init()
# screen = pygame.display.set_mode((width, height))

# class circle():
#     def __init__(self):
#         self.x = random.randint(0,width)
#         self.y = random.randint(0,height)
#         self.r = 80

#     def new(self):
#         pygame.draw.circle(screen, red, (self.x,self.y), self.r)
#         # pygame.draw.ellipse(screen, red, (self.x,self.y), self.r)

# c = []
# for i in range(circle_num):
#     c.append('c'+str(i))
#     c[i] = circle()
#     shouldprint = True
#     for j in range(len(c)):
#         if i != j:
#             dist = int(math.hypot(c[i].x - c[j].x, c[i].y - c[j].y))
#             if dist < int(c[i].r*2):
#                 shouldprint = False
#     if shouldprint:
#         c[i].new()
#         pygame.display.update()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
# points = points_generator()
# print(points, len(points))

class Sphere(pygame.sprite.Sprite):
    def __init__(self, orbit_a, orbit_r, orbit_s, rot_s, sel_r, image, parent, screen):
        super().__init__()
        self.image = pygame.image.load(image)

pygame.init()

clock = pygame.time.Clock()
width  = 1024
height = 1024
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
pygame.display.set_caption("Orbsim")
print(screen.get_rect().center)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()

