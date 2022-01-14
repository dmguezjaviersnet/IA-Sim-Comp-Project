from typing import *
from Vector3 import *
from elements3d import * 
from objects import *

MINRADIUS =1



# class obj:
#   def __init__(self, position, mass=1, radius=1,name=None):
#     self.mass = mass
#     self.position = position
#     self.radius = radius
#     self.name = name

#   def move (self , newPosition)-> None:
#     self.position = newPosition


#   def __str__(self) -> str:
#     return 'name: ' + str(self.name) + ' mass: ' + str(self.mass) + ' position: ' + str(self.position) + '  radius: ' + str(self.radius)

class Node:
  def __init__(self, region: Region, objects: List[obj] ,parent , depth:int=0, isLeafNode:bool = True ):
    self.objects = objects
    self.region = region
    self.childs = [None for i in range(8)]
    self.parent = parent
    self.depth = depth
    self.isLeafNode = True 

def giveMeOctantOfRegion (region: Region, object:obj):
  if (region.center.x < object.position.x):
    if (region.center.y < object.position.y):
      if (region.center.z < object.position.z):
        return 0 
      else: 
        return 1
    else:
      if (region.center.z < object.position.z):
        return 2
      else:
        return 3 
  else:
    if (region.center.y < object.position.y): 
      if (region.center.z < object.position.z):
        return 4 
      else:
        return 5 
    else:
      if (region.center.z < object.position.z):
        return 6 
      else:
        return 7

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


# dado una region y un punto determia si el punto esta dentro del objeto 
def ObjectInside(region: Region , vector: Vector3):
  inside = True 
  inside = inside and checkRange(region.center.x,region.radio,vector.x)
  inside = inside and checkRange(region.center.y,region.radio,vector.y)
  inside = inside and checkRange(region.center.z,region.radio,vector.z)
  return inside 

# Dada una lista de objetos y un punto como centro de referencia 
# de alguna region retorna una lista de listas de objetos de 
# cardinalidad 9, el ultimo posicion del array es para los 
# objetos que estan sobre algun plano princial de la region en cuestion
def clasifyObjects (objects: List [obj] , center: Vector3):
  #building list for clasify objects
  clasifyList = dict() 
  for obj in objects:
    octant = giveMeOctant(center=center,position=obj.position)
    if octant is None:
      if clasifyList.has_key(8):  clasifyList[8].append(obj)
      else : clasifyList[8] = [obj]
    else: 
      if clasifyList.has_key(octant):  clasifyList[octant].append(obj)
      clasifyList[octant] = clasifyList[octant] + [obj]
  return clasifyList


dirx= [-1,-1,-1,-1,1,1,1,1]
diry =[-1,-1,1,1,-1,-1,1,1]
dirz =[-1,1,-1,1,-1,1,-1,1]


# class Octree:
#   def __init__(self, region: Region, objects: List[obj]):
#     self.root = self.BuildTree(parent= None, region=region, objects=objects)

#   def BuildTree(self, parent: Node,region: Region, objects: List[obj]):
#     newRadio = region.radio // 2 
#     if len(objects) == 0 : return None 
#     if newRadio < MINRADIUS:
#       if len(objects) == 0:
#         return None
#       else:
#         return Node(region=region,objects=objects, parent=parent, isLeafNode=True)

#     objs = clasifyObjects(objects= objects, center=region.center)
#     newNode = Node(region=region,objects=objs[8],parent=parent)
#     for i in range(8):
#       if len(objs[i]) == 0:
#         continue
#       newNode.isLeafNode = False
#       newCenter = Vector3(region.center.x + dirx[i] * newRadio,region.center.x + diry[i] * newRadio, region.center.z + dirz[i] * newRadio)
#       newRegion = Region(center= newCenter,radio= newRadio)
#       newNode.childs[i] = self.BuildTree(parent=newNode , region= newRegion, objects= objs[i])
#     return newNode

#   def insertObject (self, object: obj):
#     self.root = self._insertObject(node=self.root, object=object)

#   def _insertObject(self , node: Node , object: obj):
#     if not ObjectInside(node.region,object):
#       pass 
#     newRadio = node.region.radio // 2
#     if newRadio < MINRADIUS:
#       node.objects.append(object)
#       return node
#     octant = giveMeOctant(node.region.center, object.position)
#     if node.childs[octant] is None:
#       oldCenter = node.region.center
#       newCenter = Vector3(oldCenter.x + dirx[octant], oldCenter.y +diry[octant] , oldCenter.z + dirz[octant])
#       newRegion = Region(center=newCenter,radio=newRadio)
#       node.childs[octant] = Node(newRegion,[],parent=node)
#     node.childs[octant] = self.insertObject(node.childs[octant],object)
#     return node

#   def preorden(self, node: Node):
#     for child in node.childs:
#       if child != None:
#         self.preorden(child)
#     if len(node.objects) > 0:
#       print('object:' , [str(item) for item in node.objects] , 'Region: ' , node.region)
  
#   def moveObject(self, node: Node, object: obj):
#     if not ObjectInside(node.region,object.position):
#       if node.parent is None: pass 
#       else: self.moveObject(node.parent,object)
#     octant = giveMeOctant(node.region.center,object.position)
#     if octant == 8: 
#       node.objects.append(object)
#       return None
#     if node.childs[octant] is None:
#       newRadio = node.region.radio
#       oldCenter = node.region.center
#       newCenter = Vector3(oldCenter.x + dirx[octant], oldCenter.y +diry[octant] , oldCenter.z + dirz[octant])
#       newRegion = Region(center=newCenter,radio=newRadio)
#       node.childs[octant] = Node(newRegion,[],parent=node)
#       self.moveObject(node.childs[octant],object)

#   def updateNode(self, node: Node):
#     for obj in node.objects:
#       if not ObjectInside(node.region,obj.position):
#         pass

#   def detectColision(self,node: Node):
#     if (node.region.radio <= MINRADIUS) and (len(node.objects) > 1) : return True 
#     for child in node.childs:
#       if child != None and not self.detectColision(child):
#         return True
#     return False 

# o1 = obj(position=Vector3(2,3,1), name= "object1")
# o2 = obj(position=Vector3(1,1,2), name= "object2")
# o3 = obj(position=Vector3(-1,-4,2), name= "object3")


# lstObj = [o1,o2,o3]

# # r= Region(Vector3(0,0,0),4) 

# # octree = Octree(r,lstObj)
# # octree.preorden(octree.root)
# # c = octree.detectColision(octree.root)
# list = clasifyObjects(lstObj,Vector3(0,0,0))
# print(list)


try:
    import numpy as np
except ImportError:
    np = None


class OctNode(object):
    def __init__(self, position, size, depth, data):
        self.position = position
        self.size = size
        self.depth = depth

        self.isLeafNode = True

        ## store our object, typically this will be one, but maybe more
        self.data = data

        ## might as well give it some emtpy branches while we are here.
        self.branches = [None, None, None, None, None, None, None, None]

        half = size / 2

        ## The cube's bounding coordinates
        self.lower = (position[0] - half, position[1] - half, position[2] - half)
        self.upper = (position[0] + half, position[1] + half, position[2] + half)

    def __str__(self):
        data_str = u", ".join((str(x) for x in self.data))
        return u"position: {0}, size: {1}, depth: {2} leaf: {3}, data: {4}".format(
            self.position, self.size, self.depth, self.isLeafNode, data_str
        )


class Octree(object):
    def __init__(self, worldSize, origin=(0, 0, 0), max_type="nodes", max_value=10):
        self.root = OctNode(origin, worldSize, 0, [])
        self.worldSize = worldSize
        self.limit_nodes = (max_type=="nodes")
        self.limit = max_value

    @staticmethod
    def CreateNode(position, size, objects):
        """This creates the actual OctNode itself."""
        return OctNode(position, size, objects)

    def insertNode(self, position, objData=None):
        if np:
            if np.any(position < self.root.lower):
                return None
            if np.any(position > self.root.upper):
                return None
        else:
            if position < self.root.lower:
                return None
            if position > self.root.upper:
                return None

        if objData is None:
            objData = position

        return self.__insertNode(self.root, self.root.size, self.root, position, objData)

    def __insertNode(self, root, size, parent, position, objData):
        """Private version of insertNode() that is called recursively"""
        if root is None:
            pos = parent.position

            offset = size / 2

            branch = self.__findBranch(parent, position)

            newCenter = (0, 0, 0)

            if branch == 0:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] - offset )
            elif branch == 1:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] + offset )
            elif branch == 2:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] - offset )
            elif branch == 3:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] + offset )
            elif branch == 4:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )
            elif branch == 5:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] + offset )
            elif branch == 6:
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] - offset )
            elif branch == 7:
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] + offset )

            return OctNode(newCenter, size, parent.depth + 1, [objData])

        #else: are we not at our position, but not at a leaf node either
        elif (
            not root.isLeafNode
            and
            (
                (np and np.any(root.position != position))
                or
                (root.position != position)
            )
        ):
            branch = self.__findBranch(root, position)
            newSize = root.size / 2
            root.branches[branch] = self.__insertNode(root.branches[branch], newSize, root, position, objData)

        # else, is this node a leaf node with objects already in it?
        elif root.isLeafNode:
            if (
                (self.limit_nodes and len(root.data) < self.limit)
                or
                (not self.limit_nodes and root.depth >= self.limit)
            ):
                root.data.append(objData)
            else:
                root.data.append(objData)
                objList = root.data
                root.data = None
                root.isLeafNode = False
                newSize = root.size / 2

                for ob in objList:
                    if hasattr(ob, "position"):
                        pos = ob.position
                    else:
                        pos = ob
                    branch = self.__findBranch(root, pos)
                    root.branches[branch] = self.__insertNode(root.branches[branch], newSize, root, pos, ob)
        return root

    def findPosition(self, position):
        """
        Basic lookup that finds the leaf node containing the specified position
        Returns the child objects of the leaf, or None if the leaf is empty or none
        """
        if np:
            if np.any(position < self.root.lower):
                return None
            if np.any(position > self.root.upper):
                return None
        else:
            if position < self.root.lower:
                return None
            if position > self.root.upper:
                return None
        return self.__findPosition(self.root, position)

    @staticmethod
    def __findPosition(node, position, count=0, branch=0):
        if node.isLeafNode:
            return node.data
        branch = Octree.__findBranch(node, position)
        child = node.branches[branch]
        if child is None:
            return None
        return Octree.__findPosition(child, position, count + 1, branch)

    @staticmethod
    def __findBranch(root, position):
        index = 0
        if (position[0] >= root.position[0]):
            index |= 4
        if (position[1] >= root.position[1]):
            index |= 2
        if (position[2] >= root.position[2]):
            index |= 1
        return index

    def iterateDepthFirst(self):
        """Iterate through the octree depth-first"""
        gen = self.__iterateDepthFirst(self.root)
        for n in gen:
            yield n

    @staticmethod
    def __iterateDepthFirst(root):
        """Private (static) version of iterateDepthFirst"""

        for branch in root.branches:
            if branch is None:
                continue
            for n in Octree.__iterateDepthFirst(branch):
                yield n
            if branch.isLeafNode:
                yield branch
