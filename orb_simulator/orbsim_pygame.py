from typing import List
import pygame
import gc
from simulation.orbsim_simulation_entities import SpaceDebris
from simulation.orbsim_simulation_entities import Point
from simulation.orbsim_simulation_structs import QuadTree, leaves
from sprites_and_graph_ent.eliptic_orbit import ElipticOrbit
from sprites_and_graph_ent.junk import Junk
from sprites_and_graph_ent.earth import Sphere
from tools import next_point_moving_in_elipse
from tools import BLUE
from simulation.generate_objects import *
import threading


class PygameHandler():

    def __init__(self):
        # threading.Thread.__init__(self)
        self.running = False
        self.background = pygame.image.load('./images/bg.jpg')
        self.screen_width = 1024
        self.screen_height = 1024
        # pygame.mouse.set_visible(False)
        self.screen =  pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.screen_center = (self.screen.get_rect().centerx, self.screen.get_rect().centery)
        self.orbsim_icon = pygame.image.load('./images/orbsim_logo.png')
        pygame.display.set_icon(self.orbsim_icon)
        self.main_region_rect: pygame.Rect =  pygame.Rect(self.screen.get_rect().centerx -512, self.screen.get_rect().centery - 540, 1024, 1024)
        self.orbits: List['ElipticOrbit'] = []
        self.objects: List['Junk'] = []
        self.earth = Sphere(self.screen.get_rect().centerx, self.screen.get_rect().centery)
        self.earth_group = pygame.sprite.Group()
        self.junks_group = pygame.sprite.Group()
        self.earth_group.add(self.earth)
        pygame.init()

    def generate_orbits(self, number_of_orbits):
        orbits = generate_orbits(self.screen_center, number_of_orbits)
        self.orbits = orbits
    
    def generate_objects_in_orbits(self, number_of_objects):
        self.junks_group.empty()
        self.objects.clear()
        for orb in self.orbits:
            orb_objs = generate_object_in_orbit(number_of_objects, orb)
            for obj in orb_objs:
                self.objects.append(obj)

            self.junks_group.add(orb_objs)

    def start_pygame(self):
        self.running = True
        # t1 = threading.Thread(target=self.draw, args=())
        self.draw()
        # t1.start()
        
    def draw(self):
        for o in self.orbits:
                o.draw_elipse(self.screen, (255,0,0))
        while self.running:
            self.screen.blit(self.background, (0,0))
       
            # screen.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # pygame.draw.circle(screen, BLUE, (200,300),20,0)
            # pygame.draw.rect(screen, (255,255,0), rect,2)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.earth.animate()
                    elif event.key == pygame.K_DOWN:
                        self.earth.not_animate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for o in self.junks_group.sprites():
                        o.change_selected()

            for orb in self.orbits:
                orb.draw_elipse(self.screen, (255,0,0))
            
            qTree = QuadTree(self.screen ,(Point(self.main_region_rect.topleft[0], self.main_region_rect.topleft[1]), 
                    Point(self.main_region_rect.bottomright[0], self.main_region_rect.bottomright[1])))
            
            for object in self.objects:
                qTree.insert(SpaceDebris((Point(object.rect.topleft[0], object.rect.topleft[1]), Point(object.rect.bottomright[0], object.rect.bottomright[1])),
                            0, 0, ''))
            
            qTree.insert(SpaceDebris((Point(self.earth.rect.topleft[0], self.earth.rect.topleft[1]), Point(self.earth.rect.bottomright[0], self.earth.rect.bottomright[1])),
                            0, 0, ''))

            # for leaf in leaves:
            #     leaf.find_neighbors()
            
            pygame.draw.rect(self.screen, BLUE, self.main_region_rect, 1)
       
            self.junks_group.draw(self.screen)
            self.earth_group.draw(self.screen)
        
            for obj in self.junks_group.sprites():
                # pygame.draw.circle(self.screen, (255,0,0), obj.rect.center, 3, 1)
                # obj.draw_points(self.screen)
                obj.draw_selection(self.screen)
            global leaves
            leaves.clear()
            self.junks_group.update()
            self.earth_group.update()
            self.clock.tick(30)
            pygame.display.flip()
            # gc.collect()

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
    orbits: List['ElipticOrbit'] =  generate_orbits(screen_center, 1000)
    earth = Sphere(screen.get_rect().centerx, screen.get_rect().centery)
    earth_group = pygame.sprite.Group()
    junks_group = pygame.sprite.Group()
    earth_group.add(earth)
    orbsim_icon = pygame.image.load('./images/orbsim_logo.png')
    pygame.display.set_icon(orbsim_icon)
    
    
    for o in orbits:
        new_obj = generate_object_in_orbit(10, o)
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

h = PygameHandler()
h.generate_orbits(6)
h.generate_objects_in_orbits(6)
h.start_pygame()