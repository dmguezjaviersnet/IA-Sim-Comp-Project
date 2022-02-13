from math import fabs
from heapq import heappush, heappop

from numpy import Inf
from orbsim_simulation_entities import OrbsimObj , Factory , Vector3 , Launchpad , Junk, Vector2
from typing import *
class cell: 
  def __init__(self, x , y):
    self._x = x
    self._y = y
    self._elements = [] 

  def __str__(self):
    return str(f' (%s  %s) -> %s' % (str(self._x) , str(self._y), str(self._elements))) 

class Environment:
  def __init__(self, height, width ):
    self._height = height 
    self._width = width 
    self._cells = self._generate_cells ()


  def _generate_cells (self):
    cells = [] 
    for i in range(self._height):
      cells.append([ cell(i,j) for j in range(self._width)])
    return cells

  def print (self):
    for row in self._cells:
      for col in row:
        print(col, end ='')
      print()

  def _in_range (self , x: int , y: int ):
    return ((x>=0) and (x < self._height) and (y >= 0 ) and (y < self._width))

  def getting_all_launchpad(self, pos: Vector2 , radius: int ):
    launchpad = []
    for i in range (pos.x - radius, pos.x + radius):
      for j in range (pos.y - radius, pos.y + radius):
        if self._in_range(i,j):
          for item in self._cells[i][j]._elements:
            if type(item) is Launchpad:
              launchpad.append(item)
    return launchpad

  def getting_all_factories ( self, pos : Vector2 , radius: int):
    factories = []
    for i in range (pos.x - radius, pos.x + radius):
      for j in range (pos.y - radius, pos.y + radius):
        if self._in_range(i,j):
          for item in self._cells[i][j]._elements:
            if type(item) is Factory:
              factories.append(item)
    return factories

  def give_me_adyacent_positions(self,center: Vector2):
    dirr = [-1,-1,-1,0,1,1,1,0]
    dirc = [-1,0,1,1,1,0,-1,-1] 

    for r in range(len(dirr)):
      x = center.x + dirr[r]
      y = center.y + dirc[r]
      if self._in_range(x,y):
        yield Vector2(x,y)

  def _heuristic(src : Vector2, dest: Vector2):
    return int (fabs(src.x - dest.x) + fabs(src.y - dest.y))

  def get_the_best_way (self , src:Vector2, dest: Vector2,type_element : str ):
    
    visited = [[ False for item1 in range(self._widht)]for item in range(self._height)] 
    parent = [[ None for item1 in range(self._widht)]for item in range(self._height)] 
    g= [[ Inf for item1 in range(self._widht)]for item in range(self._height)] 
    h= [[ 0 for item1 in range(self._widht)]for item in range(self._height)]
    q= []


    visited[src.x][src.y] = True
    g[src.x][src.y] = 0 
    h[src.x][src.y] = self._heuristic(src,dest)
    heappush(q,(0,src))

    while len(q) > 0:
      _ , current = heappop(q)

      if current == dest:
        return
    
      for adyacent in self.give_me_adyacent_positions(current):
        jump_width = self._heuristic(current, adyacent)

        ## haciendo relax 
        if g[current.x][current.y] + jump_width < g[adyacent.x][adyacent.y]:
          g[adyacent.x][adyacent.y] = g [current.x][current.y] + jump_width
          h[adyacent.x][adyacent.y] = self._heuristic(adyacent,dest)
          parent [adyacent.x][adyacent.y] = current

        if not visited[adyacent.x][adyacent.y]:
          heappush(q,(h[adyacent.x][adyacent.y] + g [adyacent.x][adyacent.y],adyacent))
          visited[adyacent.x][adyacent.y] = True
    
    ## obteniendo el camino 
    path = [dest]
    current = dest
    while current != dest:
      current = parent [current]
      path.append(current)
    path.reverse()
    return path


env = Environment(100,100)
env._cells[10][10]._elements.append(Factory (Vector3(10,10,10)))
env._cells[11][12]._elements.append(Factory (Vector3(11,12,10)))
env._cells[10][11]._elements.append(Factory (Vector3(10,11,10)))



factories = env.getting_all_factories(Vector2(10,10), 4)
for fact in factories:
  print (fact)
