from simulation.orbsim_simulation_entities import Vector3
import numpy as np

class Node(object):
  def __init__(self, position: Vector3, size : float, depth, data):

    # posición del nodo 
    self.position: Vector3 = position

    # tamaño del nodo 
    self.size : float= size

    # profundidad del nodo
    self.depth: int = depth

    # true si el nodo es una hoja 
    self.isLeafNode = True

    # para guardar los objetos , normalmente es uno, pero puede ser mas
    self.data = data

    # las hojas del nodo se ponen a None (inicialmente no se tiene ningún hijo) 
    self.branches = [None, None, None, None, None, None, None, None]

    # digamos que es el radio del cuadrado que representa el nodo
    half = size / 2

    ## Las coordenadad de los extremos del nodo
    self.lower = Vector3(position.x - half, position.y - half, position.z - half)
    self.upper = Vector3(position.x + half, position.y + half, position.z + half)

    def __str__(self):
      data_str = u", ".join((str(x) for x in self.data))
      return u"position: {0}, size: {1}, depth: {2} leaf: {3}, data: {4}".format(
          self.position, self.size, self.depth, self.isLeafNode, data_str
      )


class Octree(object):
  def __init__(self, world_size, origin: Vector3, max_type="nodes", max_value=10):
    '''
    inicializando el octree 
    '''

    # este es la raíz del árbol octree 
    self.root = Node(origin, world_size, 0, [])

    # este es el tamaño del espacio que va a representar el octree 
    self.world_size = world_size

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
      newCenter = Vector3.Zero()

      # tratamos de calcular el nuevo centro del octante donde se ubicara el objeto 
      if branch == 0:
        newCenter = Vector3(pos.x - offset, pos.y - offset, pos.z - offset )
      elif branch == 1:
        newCenter = Vector3(pos.x - offset, pos.y - offset, pos.z + offset )
      elif branch == 2:
        newCenter = Vector3(pos.x - offset, pos.y + offset, pos.z - offset )
      elif branch == 3:
        newCenter = Vector3(pos.x - offset, pos.y + offset, pos.z + offset )
      elif branch == 4:
        newCenter = Vector3(pos.x + offset, pos.y - offset, pos.z - offset )
      elif branch == 5:
        newCenter = Vector3(pos.x + offset, pos.y - offset, pos.z + offset )
      elif branch == 6:
        newCenter = Vector3(pos.x + offset, pos.y + offset, pos.z - offset )
      elif branch == 7:
        newCenter = Vector3(pos.x + offset, pos.y + offset, pos.z + offset )

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
    if (position.x >= root.position.x):
      index |= 4
    if (position.y >= root.position.y):
      index |= 2
    if (position.z >= root.position.z):
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
    """metodo privado para la busqueda en el octree con busqueda primero en profundidad"""

    for branch in root.branches:
      if branch is None:
        continue
      for n in Octree.__iterateDepthFirst(branch):
        yield n
      if branch.isLeafNode:
        yield branch
