from typing import List
from orbsim_simulation_entities.elements_3d import Vector3
from orbsim_simulation_entities.orbsim_obj import OrbsimObj
from orbsim_simulation_entities.satellite import Satellite

class Rocket(OrbsimObj):
  def __init__(self, position: Vector3, unique_id, weith: float = 1, diameter: int = 1, name=None, fuel:float= 100 , satellites: List['Satellite']=[]):
    super().__init__(position, unique_id, weith=weith, diameter=diameter, name=name)

    # este es el combustible del cohete 
    self.fuel: float = fuel

    # esta es la lista de satelites que contiene el cohete 
    self.satellites: Satellite = satellites

    # esta es la vida del cohete 
    self.life = 100