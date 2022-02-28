from typing import Tuple
from sprites_and_graph_ent.space_agent import SpaceAgent
from sprites_and_graph_ent.space_debris_collector import SpaceDebrisCollector

def move_towards_debris(agent: SpaceDebrisCollector, direction: Tuple[int, int]) -> bool:
    agent.vel_x = direction[0]
    agent.vel_y = direction[1]

def find_path(agent: SpaceDebrisCollector) -> bool:
    ## Usar A*
    return not any(neighbor.objects for neighbor in agent.curr_perception.neighbors)

def collect_debris(agent: SpaceDebrisCollector) -> bool:
    # Recolectar basura espacial
    pass

def change_move_direction(agent: SpaceDebrisCollector, direction: Tuple[int, int]) -> bool:
    agent.vel_x = direction[0]
    agent.vel_y = direction[1]

def reduce_speed(agent: SpaceDebrisCollector, direction: Tuple[int, int]) -> bool:
    agent.vel_x -= direction[0]
    agent.vel_y -= direction[1]

def accelerate(agent: SpaceDebrisCollector, direction: Tuple[int, int]) -> bool:
    agent.vel_x += direction[0]
    agent.vel_y += direction[1]

default_collector_actions = {
    'move_towards_debris': move_towards_debris, 
    'find_path': find_path, 
    'collect_debris': collect_debris, 
    'change_move_direction': change_move_direction, 
    'reduce_speed': reduce_speed, 
    'accelerate': accelerate, 
}

