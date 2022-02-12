from django.template import base
from orbsim_simulation_entities.orbsim_obj import OrbsimObj
from orbsim_simulation_entities.elements_3d import Vector3
import random
class Junk(OrbsimObj):

  def __init__(self,position: Vector3, unique_id, weith =1 ,diameter =1 , name= None):
    super().__init__(position,unique_id, weith=weith, diameter=diameter, name=name)

  def __str__(self) -> str:
    return f"size:{self.diameter}-position:{self.position}"


# def generateJunk():
#     junks = []
#     for _ in range(1, random.randint(5, 100)):
#         x,y,z = random.randint(1,100),random.randint(1,100),random.randint(1,100)
#         junks.append(Junk(random.randint(1,10),(x,y,z)))
#     return junks

# for junk in generateJunk():
#     print(junk)
