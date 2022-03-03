from asyncio import subprocess
from operator import le
from random import randint
from typing import List
import pygame
from sprites_and_graph_ent import ElipticOrbit, SpaceDebris, Launchpad, Satellite, SpaceDebrisCollector, space_debris_collector
from simulation.orbsim_simulation_entities import Point
from simulation.orbsim_simulation_structs import QuadTree, collisions

from sprites_and_graph_ent.earth import Sphere
from sprites_and_graph_ent.space_obj import SpaceObj
from tools import*
from tools import next_point_moving_in_elipse, round_off_wi_exceed, SELECT_BLUE_COLOR
from simulation.events import HomogeneousPoissonProcess
from simulation.generate_objects import *
import threading
import multiprocessing
import sys
import time
from orbsim_threading import ThreadWithTrace
import copy
class PygameHandler():

    def __init__(self):
        self.running = False
        self.show_orbits = False
        self.pause = False
        self.draw_qtree = False
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
        self.space_debris_group = pygame.sprite.Group()
        self.satellite_group = pygame.sprite.Group()
        self.space_debris_collector_group = pygame.sprite.Group()
        self.earth_group.add(self.earth)
        self.agents: List['SpaceDebrisCollector'] = []
        self.launchpad_factory_closing_time = None
        self.launchpad_factory_lambda = None
        self.poisson_space_creation_closing_time = None
        self.poisson_space_creation_lambda = None

        # self.subprocess = ThreadWithTrace(target=self.draw, args=())

    @property
    def number_of_satellites(self):
        return len(self.satellite_group.sprites())
    @property
    def number_of_space_debris(self):
        return len(self.space_debris_group.sprites())
    @property
    def number_of_objects(self):
        return len(self.objects)
    @property
    def number_of_orbits(self):
        return len(self.orbits)
    
    def add_new_satellite(self, satellite: 'Satellite'):
        self.objects.append(satellite)
        self.satellite_group.add(satellite)
    
    def add_new_agent(self, agent: 'SpaceDebrisCollector'):
        self.agents.append(agent)
        self.space_debris_collector_group.add(agent)
    
    def remove_agent(self, agent: 'SpaceDebrisCollector'):
        self.agents.remove(agent)
        self.space_debris_collector_group.remove(agent)
    
    def add_new_orbit(self, orbit: 'ElipticOrbit'):
        self.orbits.append(orbit)

    def create_custom_space_debris_collector(self, lifetime, capacity, fuel, perception_range, velocity):
        space_debris_collector = generate_custom_space_debris_collector(lifetime, capacity, fuel, perception_range, velocity)
        return space_debris_collector

    def create_random_space_debris_collector(self):
        space_debris_collector = generate_random_space_debris_collector()
        return space_debris_collector

    def add_new_space_debris(self, space_debris: 'SpaceDebris'):
        self.objects.append(space_debris)
        self.space_debris_group.add(space_debris)
    def remove_space_debris(self, space_debris: 'SpaceDebris'):
        self.objects.remove(space_debris)
        self.space_debris_group.remove(space_debris)

    def generate_orbits(self, number_of_orbits):
        orbits = generate_orbits(self.screen_center, number_of_orbits)
        for i in orbits:
            self.orbits.append(i)
    
    def generate_objects_in_orbits(self, number_of_objects):
        self.space_debris_group.empty()
        self.objects.clear()
        for orb in self.orbits:
            orb_objs = generate_object_in_orbit(number_of_objects, orb)
            for obj in orb_objs:
                self.objects.append(obj)
                self.space_debris_group.add(obj)
    
    def generate_new_random_space_debris(self):
        space_debris = generate_new_random_space_debris(self.orbits)
        self.space_debris_group.add(space_debris)
        self.objects.append(space_debris)
    
    def create_custom_space_debris(self, size, color):
        return generate_custom_space_debris(self.orbits, size, color)

   
    def generate_new_random_satellite(self):
        satellite =  generate_new_random_satellite(self.orbits)
        self.satellite_group.add(satellite)
        self.objects.append(satellite)

    def move_space_debris_to_orbit(self, orbit, space_debris):
        move_to_sp_other_orbit(orbit, space_debris)

    def remove_satellite(self, satellite):
        self.objects.remove(satellite)
        self.satellite_group.remove(satellite)
    
    def check_life_time_satellites(self):
        satellites_copy = self.satellite_group.sprites()
        for satellite in satellites_copy:
            if satellite.inusable:
                new_debris = SpaceDebris(satellite.pos_x, satellite.pos_y, satellite.a, satellite.b, satellite.orbit_center, satellite.size, None)
                self.add_new_space_debris(new_debris)
                self.remove_satellite(satellite)
        

    def on_collisions(self, collisions: List[Tuple['SpaceObj', 'SpaceObj']]):
        visited = []
        for obj1, obj2 in collisions:
            if isinstance(obj1, SpaceDebris) and isinstance(obj2, SpaceDebris):

                if (obj1, obj2) in visited or (obj2, obj1) in visited:
                    continue
                if abs(obj1.area - obj2.area) > 200:



                # new_debris = generate_space_debris_subdivide(obj1, obj2)
                # for d in new_debris:
                #     self.add_new_space_debris(d)
                    if obj1.area > obj2.area:
                        if obj2 in self.objects:
                            self.remove_space_debris(obj2)
                    
                #     subdivide_x = randint(2,4)
                #     subdivide_y = randint(2,4)
                #     obj1.update_surface(obj1.rect.width/subdivide_x, obj1.rect.height/subdivide_y)
                    else:
                        if obj1 in self.objects:
                            self.remove_space_debris(obj1)
                #     subdivide_x = randint(2,4)
                #     subdivide_y = randint(2,4)
                #     obj2.update_surface(obj2.rect.width/subdivide_x, obj2.rect.height/subdivide_y)
                
                else:
                    # new_debris = generate_space_debris_subdivide(obj1, obj2)
                    # for d in new_debris:
                    #     self.add_new_space_debris(d)
                    # subdivide_x_1 = randint(1,2)
                    # subdivide_y_1 = randint(1,2)
                    # subdivide_x_2 = randint(1,2)
                    # subdivide_y_2 = randint(1,2)
                    rand_ = random.random()
                    obj1.update_surface(abs(obj1.rect.width - obj2.rect.width/random.randint(4,9)), abs(obj1.rect.height - obj2.rect.width/random.randint(4,9)))
                    obj2.update_surface(abs(obj2.rect.width - obj1.rect.width/random.randint(4,9)), abs(obj2.rect.height - obj1.rect.width/random.randint(4,9)))
            elif isinstance(obj1, Satellite) and isinstance(obj2, SpaceDebris):
                obj1.life_time -= obj2.area/random.randint(6,20)
            elif isinstance(obj2, Satellite) and isinstance(obj1, SpaceDebris):
                obj2.life_time -= obj1.area/random.randint()
            
            

    def draw_path(self, path, agent):
        for pos, qt_node in enumerate(path):
            pos_x = qt_node.center_x
            pos_y = qt_node.center_y

            if pos == 0:
                pygame.draw.line(self.screen, SELECT_BLUE_COLOR, (agent.pos_x, agent.pos_y),(pos_x, pos_y), 2)

            if pos == len(path)-1:
                pygame.draw.circle(self.screen, WHITE_COLOR,(pos_x, pos_y), 2, 2)

            else:
                pygame.draw.circle(self.screen, WHITE_COLOR,(pos_x, pos_y), 2, 2)

            if pos != len(path)-1:
                new_pos_x = path[pos+1].center_x 
                new_pos_y = path[pos+1].center_y
                pygame.draw.line(self.screen, SELECT_BLUE_COLOR, (pos_x, pos_y),(new_pos_x, new_pos_y), 2)

    def start_pygame(self):
        pygame.init()
        self.running = True
        self.draw()
        # self.subprocess.start()
        # subprocess = multiprocessing.Process(target=self.draw, args=())
        # subprocess.start()
    
    def stop_pygame(self):
        # if self.is_alive():
        #     self.subprocess.kill()
        #     self.subprocess.join()
       
        # if not self.is_alive():
        #     print('thread killed')
        # if self.running :
        #     self.running = False
            pygame.quit()
        # subprocess.raise_exception()
        # self.subprocess.terminate()
    
    def pause_pygame(self):
        self.pause = not self.pause
        
    def draw_quadtree(self):
        self.draw_qtree = not self.draw_qtree

    def earth_animate(self):
        self.earth.animate()

    def draw(self):
        max_time = 0
        counter_time = 0.00
        self.screen.blit(self.background, (0,0))
        if self.launchpad_factory_closing_time and self.launchpad_factory_lambda:
            launchpad = Launchpad(self.launchpad_factory_closing_time, self.launchpad_factory_lambda)
        else:
            launchpad = Launchpad(1000, 0.5)
        
        sys.stdout = sys.__stdout__
        if self.poisson_space_creation_closing_time and self.poisson_space_creation_lambda:
            sp_poisson = HomogeneousPoissonProcess(self.poisson_space_creation_closing_time, self.poisson_space_creation_lambda)

        else:
            sp_poisson =  HomogeneousPoissonProcess(1000, 0.1)
        
        while self.running:
            # print(len(self.objects))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.earth_animate()
                    elif event.key == pygame.K_p:
                        self.pause = not self.pause
                    elif event.key == pygame.K_q:
                       self.draw_quadtree()
                    elif event.key == pygame.K_o:
                        self.show_orbits = not self.show_orbits
                    elif event.key == pygame.K_r:
                       self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for o in self.space_debris_group.sprites():
                        o.change_selected()

            if not self.pause:
                self.screen.blit(self.background, (0, 0))
                # print(launchpad.closing_time)
                # print(launchpad.lambda_value)
                # print(launchpad.closing_time)
                # Modelo de dos servidores en serie para fabricación y despegue de cohetes para la posterior puesta en órbita de los satélites que están en los mismos
                if launchpad.closing_time > round_off_wi_exceed(counter_time):
                    print(f' {launchpad.rocket_manufacturing.next_arrival_time} {launchpad.next_departure_time} {launchpad.rocket_manufacturing.next_departure_time} {counter_time}')
                    launchpad.update(counter_time, self.orbits)
                        
                    if launchpad.lauch_that_is_running and round_off_wi_exceed(launchpad.next_departure_time)  == round_off_wi_exceed(counter_time):
                        print(f'fSe lanzo el cohete {launchpad.lauch_that_is_running.rocket.rocket_id}')
                        satellite = launchpad.lauch_that_is_running.rocket.satellite
                        self.add_new_satellite(satellite)
                        launchpad.update_departure(counter_time)
                        
                # Evente de Poisson para generar nuevos objetos
                if sp_poisson.closing_time > round_off_wi_exceed(counter_time):
                    print(f'current_time{counter_time} NextPoissonEvent: {sp_poisson.next_event_time}')
                    if round_off_wi_exceed(sp_poisson.next_event_time) == round_off_wi_exceed(counter_time):
                        sp_poisson.generate_next_event()
                        new_obj = generate_new_object_in_random_orbit(self.orbits)
                        self.objects.append(new_obj)
                        self.space_debris_group.add(new_obj)

                # start = time.time()
                qTree = QuadTree(self.screen ,(Point(self.main_region_rect.topleft[0], self.main_region_rect.topleft[1]),
                        Point(self.main_region_rect.bottomright[0], self.main_region_rect.bottomright[1])), self.draw_qtree)

                qTree.insert(self.earth)

                for object in self.objects:
                    object.is_colliding = False
                    qTree.insert(object)
                
                for agent in self.agents:
                    qTree.insert(agent)
                
                leaves = []
                queue = [qTree.root]
                visited = []
                while queue:
                    curr_elem = queue.pop(0)
                    if not curr_elem.children:
                        leaves.append(curr_elem)
                    
                    else:
                        for child in curr_elem.children:
                            if child not in visited:
                                visited.append(child)
                                queue.append(child)

                global  collisions
                for leaf in leaves:
                    leaf.find_neighbors()
                    leaf.check_collisions()

                #     pygame.draw.rect(self.screen, (randint(0, 255), randint(0, 255), randint(0, 255)), 
                #                                 [leaf.bounding_box_tl[0], leaf.bounding_box_tl[1], 
                #                                 leaf.bounding_box_br[0] - leaf.bounding_box_tl[0], leaf.bounding_box_br[1] - leaf.bounding_box_tl[1]])
                
                # queue = [leaves[0]]
                # visited = []
                # while queue:
                #     curr_elem = queue.pop(0)
                #     for neighbor in curr_elem.neighbors:
                #         if neighbor not in visited:
                #             visited.append(neighbor)
                #             queue.append(neighbor)
                #             pygame.draw.rect(self.screen, (randint(0, 255), randint(0, 255), randint(0, 255)), 
                #                                 [neighbor.bounding_box_tl[0], neighbor.bounding_box_tl[1], 
                #                                 neighbor.bounding_box_br[0] - neighbor.bounding_box_tl[0], neighbor.bounding_box_br[1] - neighbor.bounding_box_tl[1]])

                # for leaf in leaves:
                #     leaf.check_collisions()
                # unique_leaves = []
                # unique_objects = []
                # for i in leaves:
                #     if i.objects:
                #         for obj in i.objects:
                #             if obj not in unique_objects:
                #                 unique_objects.append(obj)
                #                 if i not in unique_leaves:
                #                     unique_leaves.append(i)
                
                # for unique_leaf in unique_leaves:
                #     unique_leaf.find_neighbors()
                #     for neigh in unique_leaf.neighbors:
                #         pygame.draw.rect(self.screen, (255, 0, 0), 
                #                                 [neigh.bounding_box_tl[0], neigh.bounding_box_tl[1], 
                #                                 neigh.bounding_box_br[0] - neigh.bounding_box_tl[0], neigh.bounding_box_br[1] - neigh.bounding_box_tl[1]])
                    
                #     pygame.draw.circle(self.screen, (0, 255, 0),
                #             [unique_leaf.center_x, unique_leaf.center_y], 5)
                            
                # qTree.insert(self.earth)
                    # for neigh in leaf.neighbors:
                    #     print(f'leaf centered at {leaf.center_x} x and {leaf.center_y} y --------> neighbor centered at {neigh.center_x} x {neigh.center_y} y')
                    
                #     # print(len(leaf.neighbors))

                # queue = [leaves[0]]
                # visited = []
                # while queue:
                #     elem = queue.pop(0)
                #     for neigh in elem.neighbors:
                #         if not neigh in visited:
                #             visited.append(neigh)
                #             queue.append(neigh)
                #             pygame.draw.rect(self.screen, (255, 0, 0), 
                #                             [neigh.bounding_box_tl[0], neigh.bounding_box_tl[1], 
                #                             neigh.bounding_box_br[0] - neigh.bounding_box_tl[0], neigh.bounding_box_br[1] - neigh.bounding_box_tl[1]])
                
                

                # print(f'Initial leave is at {leaves[0].center_x} x and {leaves[0].center_y} y')

                # print(f'THERE ARE {len(leaves)} leaves')

                for agent in self.agents:
                    agent.options()
                    print(agent.action_target.action)
                    path = agent.path_to_target
                    if path:
                        self.draw_path(path, agent)
                    
                    # if path:
                    #     for qt_node in path:
                    #         pygame.draw.rect(self.screen, (0, 0, 255), 
                    #                             [qt_node.bounding_box_tl[0], qt_node.bounding_box_tl[1], 
                    #                             qt_node.bounding_box_br[0] - qt_node.bounding_box_tl[0], qt_node.bounding_box_br[1] - qt_node.bounding_box_tl[1]])
                                                
                            # pygame.draw.rect(self.screen, (0, 255, 0), 
                            #                     [agent.action_target.qt_node.bounding_box_tl[0], agent.action_target.qt_node.bounding_box_tl[1], 
                            #                     agent.action_target.qt_node.bounding_box_br[0] - agent.action_target.qt_node.bounding_box_tl[0], agent.action_target.qt_node.bounding_box_br[1] - agent.action_target.qt_node.bounding_box_tl[1]])
                        
                for agent in self.agents:
                    for collected in agent.collected_debris:
                        self.objects.remove(collected)
                        
                        self.space_debris_group.remove(collected)
                        print(len(self.space_debris_group.sprites()))
                        print(f'Agente 007 : Capacity: {agent.capacity} Fuel: {agent.fuel}')
                       
                    agent.collected_debris.clear()

                # qTree = QuadTree(self.screen ,(Point(self.main_region_rect.topleft[0], self.main_region_rect.topleft[1]),
                #         Point(self.main_region_rect.bottomright[0], self.main_region_rect.bottomright[1])), self.draw_qtree)
                
                # for object in self.objects:
                #     object.is_colliding = False
                #     qTree.insert(object)
                # for agent in self.agents:
                #     qTree.insert(agent)

                # pygame.draw.rect(self.screen, BLUE, self.main_region_rect, 1)
                # end = time.time()
                # if end - start > max_time: 
                #     max_time = end - start
    
                # print(max_time)
                if self.show_orbits:
                    for orb in self.orbits:
                        orb.draw_elipse(self.screen, PLUM_COLOR)

                self.space_debris_group.draw(self.screen)
                self.satellite_group.draw(self.screen)
                self.earth_group.draw(self.screen)
                self.space_debris_collector_group.draw(self.screen)

                for obj in self.objects:
                    obj.draw_collision(self.screen)
                    # pygame.draw.circle(self.screen, (255, 0, 0), obj.rect.center, 3, 1)
                    # obj.draw_points(self.screen)
                    obj.draw_selection(self.screen)
                
                leaves.clear()

                if collisions:
                    self.on_collisions(collisions)

                collisions.clear()
                self.space_debris_group.update()
                self.earth_group.update()
                self.satellite_group.update()
                self.space_debris_collector_group.update()
                self.check_life_time_satellites()
                counter_time += 0.01
                self.clock.tick(60)
                
                pygame.display.flip()
        pygame.quit()

