from dataclasses import dataclass
from sprites_and_graph_ent.satellite import Satellite

class Rocket:
    def __init__(self, satellite):
        self.rocket_id: int = id(self)
        self.satellite: 'Satellite' = satellite