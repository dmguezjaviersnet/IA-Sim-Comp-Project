from collections import defaultdict
from heapq import heappop, heappush
from math import fabs, inf
from pprint import pprint
from buildgraph import  buildgraph , rocks
import enum

class State (enum.Enum):
  WITHE =1
  GRAY = 2 
  BLACK = 3 

class Graph (object):

  def __init__(self, connections , graph: defaultdict , rows : int ,columns : int ,directed = False):
    self._graph = graph 
    self._directed = directed
    self.add_connections(connections)
    self._mask = [False] * (rows * columns + 1)
    self._parent = [-1] * (rows * columns + 1)
    self._visited = [State.WITHE] * (rows * columns + 1)
    self._g = [inf] * (rows * columns +1)
    self._h = [inf] * (rows * columns +1) 
    self._rows = rows
    self._columns = columns

  # pone en el src el valor de la heuristica calculada
  def heuristic(self, src : int , dest: int , columns: int):
    x1, y1 = src // columns , src % columns
    x2, y2 = dest // columns , dest % columns
    self._h[src] = int(fabs(x1 - x2) + fabs(y1 - y2)) 

  def __str__(self) -> str:
      return str(self._graph)

  # pone hace relax a partir de un nodo src a otro dest con un peso width
  def relax (self, src: int , dest: int , width: int):
    if self._g[src] + width < self._g[dest]:
      self._g[dest] = self._g[src] + width
      self._parent[dest] = src
      return True 
    return False

  def clearall(self):
    for i in range (self._rows * self._columns +1):
      self._parent[i] = -1
      self._mask[i] = False
      self._visited[i] = State.WITHE
      self._g[i] = inf
      self._h[i] = inf

  def astar(self,src, dest):
    self.clearall()
    q = [] 
    self._visited[src] = True
    self._g[src] = 0 
    self.heuristic(src , dest , self._columns)
    heappush(q, (0,src))

    while len(q) > 0:
      _, current = heappop(q)
      
      if current == dest:
        break
      
      for adyacent in self._graph[current]:
        neighbour , neigbourwidth = adyacent
        self.heuristic(neighbour, dest, self._columns)
        isless = self.relax(current,neighbour, neigbourwidth)

        if (self._visited[neighbour] != State.BLACK) and isless:
          heappush(q, (self._h[neighbour]+ self._g[neighbour] , neighbour))
          self._visited[neighbour] = State.GRAY
          self._parent[neighbour] = current
      
      self._visited[current] = State.BLACK

    path = [dest]
    while dest != src:
      dest = self._parent[dest]
      path.append(dest)
    path.reverse()
    return path
    

  def add_connections (self, connections): 
    for node1 , node2 in connections: 
      self.add(node1, node2) 

  def add (self,node1 , node2) :
    self._graph[node1].add(node2)
    if not self._directed:
      self._graph[node2].add(node1)
  
  def remove (self, node): 
    
    for n ,cxns in self._graph.items():
      try:
        cxns.remove(node)
      except KeyError:
        pass
    
    try:
      del self._graph[node]
    except KeyError:
      pass
  
  def is_connected (self, node1, node2):

    return node1 in self._graph and node2 in self._graph[node1]

  def find_path(self , node1, node2 , path =[]):

    path = path + [node1] 
    if node1 == node2:
      return path 
    if node1 not in  self._graph:
      return None
    for node in self._graph[node1]: 
      if node not in path:
        new_path = self.find_path(node , node2, path) 
        if new_path:
          return new_path
    return None 

  def __str__ (self):
    return '{}({})'.format(self.__class__.__name__, dict(self._graph))




class Node:
  def __init__(self, ):
    self.visited = False
    self.heuristic = 0 # h(x)
    self.realcost = 0 # g(x)
  
  def H (self): 
    return self.heuristic + self.realcost


def getconnections (G): 
  conections = set()
  for n,cxns in G.items():
    for ady , width in cxns:
      conections.add((n,ady,width))
  return conections


if __name__ == '__main__': 
  G = buildgraph(10,10,rocks)
  # pprint(conn)
  graph = Graph([], G,10,10)
  walk = graph.astar(21,79)
  pprint(walk)