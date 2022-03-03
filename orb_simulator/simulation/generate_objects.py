from typing import List
import math
from sprites_and_graph_ent.rocket import Rocket
from sprites_and_graph_ent import ElipticOrbit
from sprites_and_graph_ent import SpaceDebris, Satellite, SpaceDebrisCollector
import random
from tools import next_point_moving_in_elipse

def generate_orbits(center, number_of_orbits):
    orbits = []
    pointer = 0
    while pointer < number_of_orbits:
        
        new_orbit =  generate_new_random_orbit(center)
        if new_orbit in orbits:
            continue
        else:
            pointer +=1 
            orbits.append(new_orbit)
    return orbits

def generate_new_random_orbit(center):
    width = random.randint(100,1000)
    height = random.randint(100,850)
    new_orbit = ElipticOrbit(center, width, height)
    return new_orbit

def generate_new_orbit(center, width, height):
    return ElipticOrbit(center, width, height)

def generate_new_object_in_orbit(orbit: 'ElipticOrbit'):
    point = orbit.center
    angle =  random.randint(0,360)
    a = orbit.semi_major_axis if orbit.over_axis == 'x' else orbit.semi_minor_axis
    b = orbit.semi_minor_axis if orbit.over_axis == 'x' else orbit.semi_major_axis
    vel =  random.random() *2
    type = random.randint(1,2)
    next_point = next_point_moving_in_elipse(point,  a, b, angle)
    
    obj = SpaceDebris(next_point[0], next_point[1], a, b, point, None, None, vel if vel > 0 else 0.1)
    
    return obj

def generate_random_orbit(orbits: List['ElipticOrbit']):
    random_pos = random.randint(0,len(orbits)-1)
    return orbits[random_pos]

def generate_new_object_in_random_orbit(orbits: List['ElipticOrbit']):
    random_orbit = generate_random_orbit(orbits)
    return generate_new_object_in_orbit(random_orbit)

def generate_new_random_space_debris(orbits: List['ElipticOrbit']):
    random_orbit = orbits[random.randint(0, len(orbits)-1)]
    space_debris =  generate_space_debris_in_orbit(random_orbit)
    return space_debris

def generate_custom_space_debris(orbits: List['ElipticOrbit'], size, color):
    random_orbit = orbits[random.randint(0, len(orbits)-1)]
    point = random_orbit.center
    angle =  random.randint(0,360)
    a = random_orbit.semi_major_axis if random_orbit.over_axis == 'x' else random_orbit.semi_minor_axis
    b = random_orbit.semi_minor_axis if random_orbit.over_axis == 'x' else random_orbit.semi_major_axis
    vel =  random.random() *2
    type = random.randint(1,2)
    next_point = next_point_moving_in_elipse(point,  a, b, angle)
    
    space_debris = SpaceDebris(next_point[0], next_point[1], a, b, point, size, color, vel if vel > 0 else 0.1)
   
    return space_debris

def move_to_sp_other_orbit(orbit: 'ElipticOrbit', space_debris: 'SpaceDebris'):
    angle =  space_debris.orbit_angle
    a = orbit.semi_major_axis if orbit.over_axis == 'x' else orbit.semi_minor_axis
    b = orbit.semi_minor_axis if orbit.over_axis == 'x' else orbit.semi_major_axis
    next_point = next_point_moving_in_elipse(orbit.center,  a, b, angle)
    space_debris.move_to_orbit(next_point[0], next_point[1], a, b, orbit.center)

def generate_new_random_satellite(orbits: List['ElipticOrbit']):
    random_orbit = orbits[random.randint(0, len(orbits)-1)]
    satellite =  generate_satellite_in_orbit(random_orbit)
    return satellite

def generate_object_in_orbit(number_objects:int, orbit: 'ElipticOrbit')-> None:
    objs = []
    for _ in range(number_objects):
        space_debris = generate_space_debris_in_orbit(orbit)
        objs.append(space_debris)
    return objs

def generate_space_debris_in_orbit(orbit: 'ElipticOrbit'):
    point = orbit.center
    angle =  random.randint(0,360)
    a = orbit.semi_major_axis if orbit.over_axis == 'x' else orbit.semi_minor_axis
    b = orbit.semi_minor_axis if orbit.over_axis == 'x' else orbit.semi_major_axis
    vel =  random.random() * 2
    type = random.randint(1, 2)
    next_point = next_point_moving_in_elipse(point,  a, b, angle)
    
    space_debris = SpaceDebris(next_point[0], next_point[1], a, b, point, None, None, vel if vel > 0 else 0.1)
   
    return space_debris

def generate_satellite_in_orbit(orbit: 'ElipticOrbit'):
    point = orbit.center
    angle =  random.randint(0,360)
    a = orbit.semi_major_axis if orbit.over_axis == 'x' else orbit.semi_minor_axis
    b = orbit.semi_minor_axis if orbit.over_axis == 'x' else orbit.semi_major_axis
    vel =  random.random() *2
    type = random.randint(1,2)
    next_point = next_point_moving_in_elipse(point,  a, b, angle)
    satellite = Satellite(next_point[0], next_point[1], a, b, point, vel if vel > 0 else 0.1)
    return satellite

def generate_waiting_time(lambda_value = 0.1):
    ran_var_uni =  random.random()
    return - (1/lambda_value)*math.log(ran_var_uni)

def generate_new_rocket(orbits):
    orbit = orbits[random.randint(0, len(orbits)-1)]
    satellite = generate_satellite_in_orbit(orbit)
    rocket = Rocket(satellite)
    return rocket

def generate_space_debris_subdivide(space_debris1: 'SpaceDebris', space_debris2: 'SpaceDebris'):
    count_new_debris = random.randint(0,round(abs(space_debris1.area - space_debris2.area) % 5))
    max_size = (min(space_debris1.rect.width, space_debris2.rect.width), min(space_debris1.rect.height, space_debris2.rect.height))
    debris = []
    for i in range(count_new_debris):
        if random.randint(0,1):
            point = space_debris1.orbit_center
            angle = space_debris1.orbit_angle
            a = space_debris1.a
            b = space_debris1.b
            
        else:
            point = space_debris2.orbit_center
            angle = space_debris2.orbit_angle
            a = space_debris2.a
            b = space_debris2.b

        width =  random.randint(1, max_size[0]-1 if max_size[0] > 1 else 1)
        height = random.randint(1, max_size[1]-1 if max_size[1] > 1 else 1)
        vel =  random.random() * 2
        next_point = next_point_moving_in_elipse(point,  a, b, angle)
    
        sp = SpaceDebris(next_point[0], next_point[1], a, b, point, (width, height), None, vel if vel > 0 else 0.1)
        debris.append(sp)
    
    return debris
    
def generate_custom_space_debris_collector(lifetime, capacity, fuel, perception_range, vel):
    pos_x = random.randint(1,800)
    pos_y = random.randint(1,800)
    return SpaceDebrisCollector(pos_x, pos_y, lifetime, capacity, fuel, perception_range, vel)

def generate_space_debris_collector():
    pos_x = random.randint(1,800)
    pos_y = random.randint(1,800)
    span = 500
    capacity = 3000000
    fuel = 5000000
    collector = SpaceDebrisCollector(pos_x, pos_y, span, capacity, fuel)
    return collector