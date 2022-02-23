from typing import List
import pygame
import random
from sprites_and_graph_ent.eliptic_orbit import ElipticOrbit
from sprites_and_graph_ent.junk import Junk
from sprites_and_graph_ent.earth import Sphere
from tools import next_point_moving_in_elipse
from tools import BLUE
from simulation.generate_objects import *


def start_simulation():
    pygame.quit()
    background = pygame.image.load('./images/bg.jpg')
    screen_width = 1920
    screen_height = 1080
    screen =  pygame.display.set_mode((screen_width, screen_height))
    pygame.init()
    clock = pygame.time.Clock()
    rect: pygame.Rect =  pygame.Rect(screen.get_rect().centerx -512, screen.get_rect().centery - 541, 1024, 1024)
    screen_center = (screen.get_rect().centerx, screen.get_rect().centery)
    orbits: List['ElipticOrbit'] =  generate_orbits(screen_center, 8)
    earth = Sphere(screen.get_rect().centerx, screen.get_rect().centery)
    earth_group = pygame.sprite.Group()
    junks_group = pygame.sprite.Group()
    earth_group.add(earth)
    orbsim_icon = pygame.image.load('./images/orbsim_logo.png')
    pygame.display.set_icon(orbsim_icon)
    
    for o in orbits:
        new_obj = generate_object_in_orbit(4, o)
        junks_group.add(new_obj)
    
    while True:
        screen.blit(background, (0,0))
       
    # screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # pygame.draw.circle(screen, BLUE, (200,300),20,0)
            # pygame.draw.rect(screen, (255,255,0), rect,2)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    earth.animate()
                if event.key == pygame.K_DOWN:
                    earth.not_animate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for o in junks_group.sprites():
                        o.change_selected()
        
        
        for o in orbits:
            o.draw_elipse(screen, (255,0,0))
       
        for o in orbits:
            o.draw_elipse(screen, (255,0,0))
        
        
       
        junks_group.draw(screen)
        earth_group.draw(screen)
        
        for o in junks_group.sprites():
            pygame.draw.circle(screen, (255,0,0), o.rect.center, 3, 1)
            o.draw_points(screen)
            o.draw_selection(screen)
        
        junks_group.update()
        earth_group.update()
        clock.tick(60)
        pygame.display.flip()


