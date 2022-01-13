from typing import *
from elements3d import Vector3

class obj:
  def __init__(self, position:Vector3, unique_id, weith:float=1, diameter:int=1,name=None):
    self.weith = weith
    self.position = position
    self.diameter = diameter
    self.name = name
    self.unique_id = unique_id

  def move (self , newPosition)-> None:
    self.position = newPosition


  def __str__(self) -> str:
    return 'name: ' + str(self.name) + ' weith: ' + str(self.weith) + ' position: ' + str(self.position) + '  diameter: ' + str(self.radius)

class Rocket(obj):
    def __init__(self, fuel:int , satellites: List['Satellite'] = []) -> None:
      self.fuel = fuel
      self.satellites = satellites
      self.life = 100