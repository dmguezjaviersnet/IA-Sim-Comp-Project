from sprites_and_graph_ent.orbit_obj import OrbitObj
from tools import SOLID_BLUE_COLOR
class SpaceDebris(OrbitObj):
    
    def __init__(self, pos_x, pos_y, a, b, orbit_center, mass: int, vel: int = 0.5):
        super().__init__(pos_x, pos_y, a, b, orbit_center, vel)
        self.default_color = SOLID_BLUE_COLOR
        self.image.fill(self.default_color)
        self.mass = mass
    
    @property
    def area(self):
        return self.rect.width * self.rect.height
    
    