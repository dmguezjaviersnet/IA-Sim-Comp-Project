from typing import List
import math
from urllib3 import Retry
from sprites_and_graph_ent.rocket import Rocket
from sprites_and_graph_ent import ElipticOrbit
from sprites_and_graph_ent import SpaceDebris, Satellite
import random
from tools import next_point_moving_in_elipse

def generate_orbits(center, number_of_orbits):
    orbits = []
    pointer = 0
    while pointer < number_of_orbits:
        
        width = random.randint(100,1000)
        height = random.randint(100,850)
        new_orbit = ElipticOrbit(center, width, height)
        if new_orbit in orbits:
            continue
        else:
            pointer +=1 
            orbits.append(new_orbit)
    return orbits
    

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
    if random.randint(0,1):
         obj = SpaceDebris(next_point[0], next_point[1], a, b, point, vel if vel > 0 else 0.1)
    else:
        obj = Satellite(next_point[0], next_point[1], a, b, point, vel if vel > 0 else 0.1)
    return obj

def generate_random_orbit(orbits: List['ElipticOrbit']):
    random_pos = random.randint(0,len(orbits)-1)
    return orbits[random_pos]

def generate_new_object_in_random_orbit(orbits: List['ElipticOrbit']):
    random_orbit = generate_random_orbit(orbits)
    return generate_new_object_in_orbit(random_orbit)

def generate_object_in_orbit(number_objects:int, orbit: 'ElipticOrbit')-> None:
    point = orbit.center
    objs = []
    for _ in range(number_objects):
        angle =  random.randint(0,360)
        a = orbit.semi_major_axis if orbit.over_axis == 'x' else orbit.semi_minor_axis
        b = orbit.semi_minor_axis if orbit.over_axis == 'x' else orbit.semi_major_axis
        vel =  random.random() *2
        type = random.randint(1,2)
        next_point = next_point_moving_in_elipse(point,  a, b, angle)
        junk = SpaceDebris(next_point[0], next_point[1], a, b, point, vel if vel > 0 else 0.1)
        objs.append(junk)
    return objs

def generate_satellite_in_orbit(orbit: 'ElipticOrbit'):
    point = orbit.center
    angle =  random.randint(0,360)
    a = orbit.semi_major_axis if orbit.over_axis == 'x' else orbit.semi_minor_axis
    b = orbit.semi_minor_axis if orbit.over_axis == 'x' else orbit.semi_major_axis
    vel =  random.random() *2
    type = random.randint(1,2)
    next_point = next_point_moving_in_elipse(point,  a, b, angle)
    if random.randint(0,1):
         obj = SpaceDebris(next_point[0], next_point[1], a, b, point, vel if vel > 0 else 0.1)
    else:
        obj = Satellite(next_point[0], next_point[1], a, b, point, vel if vel > 0 else 0.1)
    return obj

def generate_waiting_time():
    lambd = 0.04
    ran_var_uni =  random.random()
    return - (1/lambd)*math.log(ran_var_uni)

def generate_new_rocket(orbits):
    orbit = random.randint(0, len(orbits))
    point = orbit.center
    angle =  random.randint(0,360)
    a = orbit.semi_major_axis if orbit.over_axis == 'x' else orbit.semi_minor_axis
    b = orbit.semi_minor_axis if orbit.over_axis == 'x' else orbit.semi_major_axis
    vel =  random.random() *2
    type = random.randint(1,2)
    next_point = next_point_moving_in_elipse(point,  a, b, angle)
    satellite = Satellite(next_point[0], next_point[1], a, b, point, vel if vel > 0 else 0.1)
    rocket = Rocket(satellite)
    return rocket
