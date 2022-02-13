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

  def getting_all_factories ( self, pos : Vector2 , radius: int):
    factories = []
    for i in range (pos.x - radius, pos.x + radius):
      for j in range (pos.y - radius, pos.y + radius):
        if self._in_range(i,j):
          for item in self._cells[i][j]._elements:
            if type(item) is Factory:
              factories.append(item)

env = Environment(1000,1000)
# env.print()