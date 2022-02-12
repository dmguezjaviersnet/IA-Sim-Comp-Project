from simulation.orbsim_simulation_entities.elements_3d import Vector3
from simulation.orbsim_simulation_entities.orbsim_obj import OrbsimObj

class Satellite(OrbsimObj):
  def __init__(self, position: Vector3, unique_id, weith: float = 1, diameter: int = 1, name=None):
    super().__init__(position, unique_id, weith=weith, diameter=diameter, name=name)
    '''
    inicializacion de los satelites , se llama a la clase padre 
    para inicializar los valores que se pasan en los parametros 
    '''