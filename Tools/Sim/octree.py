
from typing import List
from Vector3 import *

class Node:
  def __init__(self, region : Region, objects):
    self.objects = objects
    self.region = region
    self.childs = []
    self.parent = None

class Objects:
  def __init__(self, mass, position, radius= 1):
    self.mass = mass
    self.position = position
    self.radius = radius


def giveMeOctant (center : Vector3 , position: Vector3):
  newpos = position - center
  newpos = newpos.sig()
  if newpos.x == 0 or newpos.y == 0 or newpos.z == 0:
    return None
  xx = newpos.x if newpos.x > 0 else 0
  yy = newpos.y if newpos.y > 0 else 0
  zz = newpos.z if newpos.z > 0 else 0
  return xx * 4 | yy * 2 | zz
  

class Region:
  def __init__(self, center: Vector3 , radio : int) -> None:
    self.center = center
    self.radio = radio

def clasifyObjects (objects: List [Objects] , center: Vector3):
  #building list for clasify objects
  clasifyList = [[] for i in range (9)] 
  for obj in objects:
    octant = giveMeOctant(center=center,position=obj.position)
    if octant is None:
      clasifyList[8].append(obj)
    else: 
      clasifyList[octant].append(obj)
  return clasifyList

class Octree:
  def __init__(self, objects):
    self.root = Node(objects)

  def BuildTree(self, node: Node, objects: List[Objects]):
    obj = clasifyObjects(objects= objects, center=node.region)


a = Vector3(-2,-3,4)
b = Vector3(5,6,7)

center = Vector3(0,0,0)
print (giveMeOctant(center, position=a))