from sprites_and_graph_ent import ElipticOrbit
from sprites_and_graph_ent import Junk
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
    junk = Junk(next_point[0], next_point[1], 'satellite' if type == 1 else 'rock', a, b, point, vel if vel > 0 else 0.1)
    return junk

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
        junk = Junk(next_point[0], next_point[1], 'satellite' if type == 1 else 'rock', a, b, point, vel if vel > 0 else 0.1)
        objs.append(junk)
    return objs


