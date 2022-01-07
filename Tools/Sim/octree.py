
from typing import List
from Vector3 import *

MINRADIUS =1

class Region:
  def __init__(self, center: Vector3 , radio : int) -> None:
    self.center = center
    self.radio = radio
  
  def __str__(self) -> str:
    return 'center :' + str(self.center)  + '  radio: ' + str(self.radio)

class Objects:
  def __init__(self, position, mass=1, radius=1,name=None):
    self.mass = mass
    self.position = position
    self.radius = radius
    self.name = name

  def __str__(self) -> str:
    return 'name: ' + str(self.name) + ' mass: ' + str(self.mass) + ' position: ' + str(self.position) + '  radius: ' + str(self.radius)

class Node:
  def __init__(self, region : Region, objects : List[Objects] ,parent:None):
    self.objects = objects
    self.region = region
    self.childs = [None for i in range(8)]
    self.parent = parent

def giveMeOctant (center : Vector3 , position: Vector3):
  newpos = position - center
  newpos = newpos.sig()
  if newpos.x == 0 or newpos.y == 0 or newpos.z == 0:
    return None
  xx = newpos.x if newpos.x > 0 else 0
  yy = newpos.y if newpos.y > 0 else 0
  zz = newpos.z if newpos.z > 0 else 0
  return xx * 4 | yy * 2 | zz

def ObjectInside (region: Region , vector: Vector3):
  if region.center.x < vector.x and region.center.y < vector.y n

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


dirx= [-1,-1,-1,-1,1,1,1,1]
diry =[-1,-1,1,1,-1,-1,1,1]
dirz =[-1,1,-1,1,-1,1,-1,1]


class Octree:
  def __init__(self, region: Region, objects: List[Objects]):
    self.root = self.BuildTree(parent= None, region=region, objects=objects)

  def BuildTree(self, parent: Node,region: Region, objects: List[Objects]):
    newRadio = region.radio // 2 
    if len(objects) == 0 : return None 
    if newRadio < MINRADIUS:
      if len(objects) == 0:
        return None
      else: return Node(region=region,objects=objects, parent=parent)

    objs = clasifyObjects(objects= objects, center=region.center)
    newNode = Node(region=region,objects=objs[8],parent=parent)
    for i in range(8):
      if len(objs[i]) == 0 : continue
      newCenter = Vector3(region.center.x + dirx[i] * newRadio,region.center.x + diry[i] * newRadio, region.center.z + dirz[i] * newRadio)
      newRegion = Region(center= newCenter,radio= newRadio)
      newNode.childs[i] = self.BuildTree(parent=newNode , region= newRegion, objects=objs[i])
    return newNode
  
  def preorden (self, node: Node):
    for child in node.childs:
      if child != None:
        self.preorden(child)
    if len(node.objects) > 0:
      print('object:' , [str(item) for item in node.objects ] , 'Region: ' , node.region)


# o1 = Objects(position=Vector3(2,6,7), name= "object1")
# o2 = Objects(position=Vector3(1,7,2), name= "object2")
# o3 = Objects(position=Vector3(-1,-6,7), name= "object3")
# o4 = Objects(position=Vector3(4,-1,-8), name= "object4")
# o5 = Objects(position=Vector3(3,-6,7), name= "object5")
# o6 = Objects(position=Vector3(2,4,-2), name= "object6")

# lstObj = [o1,o2,o3,o4,o5,o6]
# objecs = clasifyObjects(lstObj,Vector3(0,0,0))

# for i in range(len(objecs)):
#   for item in objecs[i]:
#     print(item.position)

# region = Region(Vector3(0,0,0),8)
# octree = Octree(region,lstObj)

# octree.preorden(octree.root)

# center = Vector3(0,0,0)
# for item in lstObj:
#   octant = giveMeOctant(center,item.position)
#   print(octant)