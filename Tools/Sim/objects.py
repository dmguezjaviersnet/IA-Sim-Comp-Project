from typing import *
from elements3d import Vector3
import uuid
import simpy

class obj:
  def __init__(self, position:Vector3, unique_id, weith:float=1, diameter:int=1,name=None):
    self.weith = weith
    self.position = position
    self.diameter = diameter
    self.name = name
    self.unique_id = unique_id

  def move (self, env: simpy.Environment)-> None:
    while True:
      yield env.timeout(200)
      self.position = Vector3.random()
      print ('El objeto %s se ha movido a la posicion %s' %(str(self.unique_id), str(self.position)))


  def __str__(self) -> str:
    return 'name: ' + str(self.name) + ' weith: ' + str(self.weith) + ' position: ' + str(self.position) + '  diameter: ' + str(self.radius)

class Rocket(obj):
  def __init__(self, position: Vector3, unique_id, weith: float = 1, diameter: int = 1, name=None, fuel:float= 100 , satellites: List['Satellite']=[]):
    super().__init__(position, unique_id, weith=weith, diameter=diameter, name=name)
    self.fuel = fuel
    self.satellites = satellites
    self.life = 100

class Satellite(obj):
  def __init__(self, position: Vector3, unique_id, weith: float = 1, diameter: int = 1, name=None):
    super().__init__(position, unique_id, weith=weith, diameter=diameter, name=name)


def generateObj ():
  unique_id = uuid.uuid4()
  position = Vector3.random()
  new_obj = obj(position=position,unique_id= unique_id)
  return new_obj