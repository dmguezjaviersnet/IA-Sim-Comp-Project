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

env = Environment(1000,1000)
# env.print()