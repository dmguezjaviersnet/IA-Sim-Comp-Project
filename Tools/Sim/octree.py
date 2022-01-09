from typing import *
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

  def move (self , newPosition)-> None:
    self.position = newPosition


  def __str__(self) -> str:
    return 'name: ' + str(self.name) + ' mass: ' + str(self.mass) + ' position: ' + str(self.position) + '  radius: ' + str(self.radius)

class Node:
  def __init__(self, region : Region, objects : List[Objects] ,parent , depth:int=0 ):
    self.objects = objects
    self.region = region
    self.childs = [None for i in range(8)]
    self.parent = parent
    self.depth = depth
    self.isLeafNode = True 

def giveMeOctant (center : Vector3 , position: Vector3):
  newpos = position - center
  newpos = newpos.sig()
  if newpos.x == 0 or newpos.y == 0 or newpos.z == 0:
    return None
  xx = newpos.x if newpos.x > 0 else 0
  yy = newpos.y if newpos.y > 0 else 0
  zz = newpos.z if newpos.z > 0 else 0
  return xx * 4 | yy * 2 | zz


def checkRange (c:int , r:int ,p:int):
  return (p <= (c + r)) and (p >= (c - r)) 

def ObjectInside (region: Region , vector: Vector3):
  inside = True 
  inside = inside and checkRange(region.center.x,region.radio,vector.x)
  inside = inside and checkRange(region.center.y,region.radio,vector.y)
  inside = inside and checkRange(region.center.z,region.radio,vector.z)
  return inside 


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

  def insertObject (self, object: Objects):
    self.root = self._insertObject(node=self.root, object=object)

  def _insertObject (self , node: Node , object: Objects):
    if not ObjectInside(node.region,object):
      pass 
    newRadio = node.region.radio // 2
    if newRadio < MINRADIUS:
      node.objects.append(object)
      return node
    octant = giveMeOctant(node.region.center, object.position)
    if node.childs[octant] is None:
      oldCenter = node.region.center
      newCenter = Vector3(oldCenter.x + dirx[octant], oldCenter.y +diry[octant] , oldCenter.z + dirz[octant])
      newRegion = Region(center=newCenter,radio=newRadio)
      node.childs[octant] = Node(newRegion,[],parent=node)
    node.childs[octant] = self.insertObject(node.childs[octant],object)
    return node

  def preorden (self, node: Node):
    for child in node.childs:
      if child != None:
        self.preorden(child)
    if len(node.objects) > 0:
      print('object:' , [str(item) for item in node.objects] , 'Region: ' , node.region)
  
  def moveObject(self, node: Node, object: Objects):
    if not ObjectInside(node.region,object.position):
      if node.parent is None: pass 
      else: self.moveObject(node.parent,object)
    octant = giveMeOctant(node.region.center,object.position)
    if octant == 8: 
      node.objects.append(object)
      return None
    if node.childs[octant] is None:
      newRadio = node.region.radio
      oldCenter = node.region.center
      newCenter = Vector3(oldCenter.x + dirx[octant], oldCenter.y +diry[octant] , oldCenter.z + dirz[octant])
      newRegion = Region(center=newCenter,radio=newRadio)
      node.childs[octant] = Node(newRegion,[],parent=node)
      self.moveObject(node.childs[octant],object)

  def updateNode(self, node: Node):
    for obj in node.objects:
      if not ObjectInside(node.region,obj.position):
        pass

  def detectColision (self,node: Node):
    if len(node.objects) > 1 : return True 
    for child in node.childs:
      if child != None and not self.detectColision(child):
        return True
    return False 




o1 = Objects(position=Vector3(2,3,1), name= "object1")
o2 = Objects(position=Vector3(1,1,2), name= "object2")
o3 = Objects(position=Vector3(-1,-4,2), name= "object3")


lstObj = [o1,o2,o3]

r = Region(Vector3(0,0,0),4) 

octree = Octree(r,lstObj)
octree.preorden(octree.root)
