from typing import *
from Vector3 import *
from elements3d import * 
from objects import *

MINRADIUS =1


class Node:
  def __init__(self, region: Region, objects: List[obj] ,parent , depth:int=0, isLeafNode:bool = True ):
    self.objects = objects
    self.region = region
    self.childs = [None for i in range(8)]
    self.parent = parent
    self.depth = depth
    self.isLeafNode = True 

# def giveMeOctantOfRegion (region: Region, object:obj):
#   if (region.center.x < object.position.x):
#     if (region.center.y < object.position.y):
#       if (region.center.z < object.position.z):
#         return 0 
#       else: 
#         return 1
#     else:
#       if (region.center.z < object.position.z):
#         return 2
#       else:
#         return 3 
#   else:
#     if (region.center.y < object.position.y): 
#       if (region.center.z < object.position.z):
#         return 4 
#       else:
#         return 5 
#     else:
#       if (region.center.z < object.position.z):
#         return 6 
#       else:
#         return 7

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


# dado una region y un punto determina si el punto esta dentro del objeto 
def ObjectInside(region: Region , vector: Vector3):
  inside = True 
  inside = inside and checkRange(region.center.x,region.radio,vector.x)
  inside = inside and checkRange(region.center.y,region.radio,vector.y)
  inside = inside and checkRange(region.center.z,region.radio,vector.z)
  return inside 

# Dada una lista de objetos y un punto como centro de referencia 
# de alguna region retorna una lista de listas de objetos de 
# cardinalidad 9, el ultimo posición del array es para los 
# objetos que están sobre algún plano principal de la region en cuestión
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


class Node(object):
    def __init__(self, position, size, depth, data):

        # posición del nodo 
        self.position = position

        # tamaño del nodo 
        self.size = size

        # profundidad del nodo
        self.depth = depth

        # true si el nodo es una hoja 
        self.isLeafNode = True

        ## para guardar los objetos , normalmente es uno, pero puede ser mas
        self.data = data

        ## las hojas del nodo se ponen a None (inicialmente no se tiene ningún hijo) 
        self.branches = [None, None, None, None, None, None, None, None]

        half = size / 2

        ## Las coordenadad de los extremos del nodo
        self.lower = (position[0] - half, position[1] - half, position[2] - half)
        self.upper = (position[0] + half, position[1] + half, position[2] + half)

    def __str__(self):
        data_str = u", ".join((str(x) for x in self.data))
        return u"position: {0}, size: {1}, depth: {2} leaf: {3}, data: {4}".format(
            self.position, self.size, self.depth, self.isLeafNode, data_str
        )


class Octree(object):
    def __init__(self, worldSize, origin=(0, 0, 0), max_type="nodes", max_value=10):
        '''
        inicializando el octree 
        '''

        # este es la raíz del árbol octree 
        self.root = Node(origin, worldSize, 0, [])

        # este es el tamaño del espacio que va a representar el octree 
        self.worldSize = worldSize

        # el limite de los nodos 

        self.limit_nodes = (max_type=="nodes")
        
        # el limite del octree 
        self.limit = max_value

    @staticmethod
    def CreateNode(position, size, objects):
        """Este crea al nodo actual el mismo"""
        return Node(position, size, objects)

    # esto es para insertar un objeto nuevo en el octree 
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
        """
        método privado para insertar elementos en el octree
        """
        if root is None:

            # en la variable pos ponemos la posición del padre
            pos = parent.position

            # calculamos el offset (que es como el "radio" del cubo)
            offset = size / 2

            # obtenemos la rama (octante) donde se insertara el nuevo objeto  
            branch = self.__findBranch(parent, position)

            # inicializamos un nuevo centro 
            newCenter = (0, 0, 0)

            # tratamos de calcular el nuevo centro del octante donde se ubicara el objeto 
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

            # se retorna un nuevo nodo con las nuevas dimensiones 
            return Node(newCenter, size, parent.depth + 1, [objData])

        #else: no estamos en nuestra posición, pero tampoco en una hoja
        elif (
            not root.isLeafNode
            and
            (
                (np and np.any(root.position != position))
                or
                (root.position != position)
            )
        ):
            # buscar la rama en la que s insertaria 
            branch = self.__findBranch(root, position)

            # se calcula el nuevo size 
            newSize = root.size / 2

            # se crea el nuevo octree con los objetos dentro de esta nueva region
            # y se asigna como hijo en el branch que le corresponde 
            root.branches[branch] = self.__insertNode(root.branches[branch], newSize, root, position, objData)


        # else , es este un nodo hoja con objetos todavía en el
        elif root.isLeafNode:
            if (
                (self.limit_nodes and len(root.data) < self.limit)
                or
                (not self.limit_nodes and root.depth >= self.limit)
            ):
                # se añade el nuevo objeto a la data del node 
                root.data.append(objData)
            else:
                
                # se añade el objeto a la data del nodo
                root.data.append(objData)

                #se crea una nueva variable y se la asigna la lista de data del nodo  
                objList = root.data

                # Se desreferencia la lista d e data del nodo 
                root.data = None

                # el nodo deja de ser una hoja 
                root.isLeafNode = False

                # se calcula el nuevo size del nodo 
                newSize = root.size / 2

                # se recorre la lista de objetos y se crean los nodos 
                # con una profundidad mayor 
                for ob in objList:
                    if hasattr(ob, "position"):
                        pos = ob.position
                    else:
                        pos = ob
                    
                    # se busca el octante donde se insertara el nuevo objeto
                    branch = self.__findBranch(root, pos)

                    # se crean los nuevos branch con los sub_octree que le corresponden
                    root.branches[branch] = self.__insertNode(root.branches[branch], newSize, root, pos, ob)
        
        # se retorna el root modificado 
        return root

    # retorna los objetos que están en una posición dada 
    def findPosition(self, position):
        """
        Búsqueda básica que encuentra el nodo hoja que contiene la posición especificada
        Devuelve los objetos secundarios de la hoja, o Ninguno si la hoja está vacía o ninguno 
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
        # si el nodo es una hoja se retorna la data que contiene 
        if node.isLeafNode:
            return node.data
        
        # se calcula el octante a buscar  
        branch = Octree.__findBranch(node, position)
        
        # se obtiene el sub_octree en el cual están los posibles nodos a buscar 
        child = node.branches[branch]
        if child is None:
            return None
        
        # se manda a buscar en el nodo hijo donde potencialmete se encuentren los elementos
        return Octree.__findPosition(child, position, count + 1, branch)

    # encuentra el octante dado una rama determinada
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

    # iteracion en profundidad primero 
    def iterateDepthFirst(self):
        """iterar en el octree en profundidad primero"""
        gen = self.__iterateDepthFirst(self.root)
        for n in gen:
            yield n

    # metodo privado patra iterar primero en profundidad
    @staticmethod
    def __iterateDepthFirst(root):
        """private metodo para la busqueda en el octree con busqueda primero en profundidad"""

        for branch in root.branches:
            if branch is None:
                continue
            for n in Octree.__iterateDepthFirst(branch):
                yield n
            if branch.isLeafNode:
                yield branch
