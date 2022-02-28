from cmath import sqrt
from sprites_and_graph_ent.space_debris_collector import SpaceDebrisCollector

def detect_space_debris(agent: SpaceDebrisCollector) -> bool:
    return any(neighbor.objects for neighbor in agent.curr_perception.neighbors)

def check_possible_collision(agent: SpaceDebrisCollector):
    # analizar si es posible que el agente choque con basura si sigue moviéndose en esa dirección.
    pass

def check_remaining_space(agent: SpaceDebrisCollector) -> bool:
    return agent.capacity == 0

def check_fuel_tank(agent: SpaceDebrisCollector) -> bool:
    return agent.fuel == 0

def check_life_time(agent: SpaceDebrisCollector) -> bool:
    return agent.life_span == 0

def at_max_speed(agent: SpaceDebrisCollector) -> bool:
    return sqrt(agent.vel_x**2 + agent.vel_y**2) >= 25

def at_edge_of_map(agent: SpaceDebrisCollector) -> bool:
    return agent.pos_x == 0 or agent.pos_x == 1023 or agent.pos_y == 0 or agent.pos_y == 1023

default_collector_rules = {
    'detect_space_debris': detect_space_debris,
    'check_possible_collision': check_possible_collision,
    'check_remaining_space': check_remaining_space,
    'check_fuel_tank': check_fuel_tank,
    'check_life_time': check_life_time,
    'at_max_speed': at_max_speed,
    'at_edge_of_map': at_edge_of_map,
}
