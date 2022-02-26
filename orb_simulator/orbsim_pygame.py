from typing import List
import pygame
from orb_simulator.sprites_and_graph_ent import satellite
from simulation.orbsim_simulation_entities import Point
from simulation.orbsim_simulation_structs import QuadTree, leaves
from sprites_and_graph_ent import ElipticOrbit, SpaceDebris, Launchpad
from sprites_and_graph_ent.earth import Sphere
from tools import*
from tools import next_point_moving_in_elipse, round_off_wi_exceed
from simulation.events import *
from simulation.generate_objects import *
import threading
import sys
import time

class PygameHandler(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False
        self.pause = False
        self.screen_width = 1024
        self.screen_height = 1024
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load('./images/bg.jpg')
        self.orbsim_icon = pygame.image.load('./images/orbsim_logo.png')
        self.screen_center = (self.screen.get_rect().centerx, self.screen.get_rect().centery)
        self.main_region_rect = pygame.Rect(self.screen.get_rect().centerx -510, self.screen.get_rect().centery - 510, 1024, 1024)
        pygame.display.set_icon(self.orbsim_icon)
        pygame.display.set_caption('OrbSimulator')
        self.clock = pygame.time.Clock()
        # pygame.mouse.set_visible(False)
        self.orbits: List['ElipticOrbit'] = []
        self.objects: List['SpaceDebris'] = []
        self.earth = Sphere(self.screen.get_rect().centerx, self.screen.get_rect().centery)
        self.earth_group = pygame.sprite.Group()
        self.junks_group = pygame.sprite.Group()
        self.earth_group.add(self.earth)
       
    def add_new_satellite(self, satellite: 'Satellite'):
        self.objects.append(satellite)
        self.junks_group.add(satellite)

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
                self.junks_group.add(obj)

    def start_pygame(self):
        self.running = True
        t1 = threading.Thread(target=self.draw, args=())
        t1.start()
        
    def draw(self):
        pygame.init()
        max_time = 0
        counter_time = 0.00
        self.screen.blit(self.background, (0,0))
        
        launchpad =  Launchpad(1000)
        sys.stdout = sys.__stdout__
        new_object_event = poisson_process_homogeneous(1000,0.1)
        start = time.time()
        draw_qtree = False
        while self.running:
           
            # print(len(self.objects))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.earth.animate()
                    elif event.key == pygame.K_p:
                        self.pause = not self.pause
                    elif event.key == pygame.K_q:
                        draw_qtree = not draw_qtree
                   
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for o in self.junks_group.sprites():
                        o.change_selected()
            if not self.pause:
                self.screen.blit(self.background, (0, 0))

                if launchpad.time_of_occurrence < counter_time:
                    
                    if round_off_wi_exceed(launchpad.next_arrival_time) == round_off_wi_exceed(counter_time):
                        new_rocket = generate_new_rocket(self.orbits)
                        if not launchpad.lauch_that_is_running:
                        launchpad.lauch_that_is_running = new_rocket
                    if launchpad.lauch_that_is_running and round_off_wi_exceed(launchpad.next_departure_time)  == round_off_wi_exceed(counter_time):
                        print(f'fSe lanzo el cohete {launchpad.lauch_that_is_running.rocket_id}')
                        satellite = launchpad.lauch_that_is_running.satellite
                        self.add_new_satellite(satellite)
                        launchpad.lauch_that_is_running = None
                        if launchpad.rocket_in_queue:
                            next_launch = launchpad.rocket_in_queue.pop(0)
                            launchpad.lauch_that_is_running = next_launch
                            launchpad.generate_next_departure(counter_time)
                            
                        

                if new_object_event:
                    end = time.time()
                    comm = end - start
                    current_event = new_object_event[0]
                    # print(current_event.ocurrence_time)
                    # print(comm)
                    print(round_off_wi_exceed(counter_time))
                    if round_off_wi_exceed(current_event.ocurrence_time) == round_off_wi_exceed(counter_time):
                        print(current_event.ocurrence_time)
                        new_obj = generate_new_object_in_random_orbit(self.orbits)
                        self.objects.append(new_obj)
                        self.junks_group.add(new_obj)
                        new_object_event.pop(0)
                        print(len(self.objects))
                for orb in self.orbits:
                    orb.draw_elipse(self.screen, (255,0,0))

                # start = time.time()
                qTree = QuadTree(self.screen ,(Point(self.main_region_rect.topleft[0], self.main_region_rect.topleft[1]),
                        Point(self.main_region_rect.bottomright[0], self.main_region_rect.bottomright[1])), draw_qtree)

                for object in self.objects:
                    object.is_colliding = False
                    qTree.insert(object)

                qTree.insert(self.earth)

                global leaves
                for leaf in leaves:
                    leaf.check_collisions()
                # pygame.draw.rect(self.screen, BLUE, self.main_region_rect, 1)
                # end = time.time()
                # if end - start > max_time: 
                #     max_time = end - start
    
                # print(max_time)
                for orb in self.orbits:
                    orb.draw_elipse(self.screen, PLUM_COLOR)
                self.junks_group.draw(self.screen)
                self.earth_group.draw(self.screen)

                for obj in self.objects:
                    obj.update_color()
                    # pygame.draw.circle(self.screen, (255, 0, 0), obj.rect.center, 3, 1)
                    obj.draw_points(self.screen)
                    obj.draw_selection(self.screen)

                leaves.clear()

                self.junks_group.update()
                self.earth_group.update()
                counter_time += 0.01
                self.clock.tick(60)
                
                pygame.display.flip()
        pygame.quit()