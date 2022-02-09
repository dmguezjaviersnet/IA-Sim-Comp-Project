import simpy

from orbsim_simulation_entities import OrbsimObj , Factory , Vector3 , Launchpad

class Handler:
  def __init__(self,world_size = 1024,depth = 10,amount_initial_obj= 100):
    self._world_size = world_size
    self._amount_initial_obj = amount_initial_obj
    self._amount_rockets = 10
    self._amount_launchpads =2
    self._amount_factories = 4 
    self._objects = self._generate_objects() 
    self._factories = self._generate_factories()
    self._launchpads = self._generate_launchpads()
    self._env = simpy.Environment()

  def _generate_objects(self):
    return [OrbsimObj.randomObject(self.world_size) for i in range (self.world_size)]
  
  def _generate_factories(self):
    return [Factory(Vector3.random(self._amount_factories))]

  def _generate_launchpads(self):
    return [Launchpad(self._env) for i in range(self._amount_launchpads)]

  def start(self):
    self._env.run()
