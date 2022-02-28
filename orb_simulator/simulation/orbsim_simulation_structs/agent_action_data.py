from simulation.orbsim_simulation_structs import QTNode
from sprites_and_graph_ent.space_debris import SpaceDebris

class AgentActionData:

    def __init__(self, area: int, distance: int, qt_node: QTNode, object: SpaceDebris, action: str) -> None:
        self.area = area
        self.distance = distance
        self.qt_node = qt_node
        self.object = object
        self.action = action

    def __lt__(self, other: 'AgentActionData'):
        return True if self.area < other.area else self.distance < other.distance if self.area == other.area else False