import random

class Vector3:
  def __init__(self, x:int , y:int, z:int) -> None:
    self.x: int = x 
    self.y: int = y
    self.z: int = z
  
  def __eq__(self, other: 'Vector3'):
    return self.x == other.x and self.y == other.y and self.z == other.z 

  def __add__ (self , other):
    return Vector3(self.x + other.x , self.y + other.y , self.z + other.z)
  
  def __sub__ (self , other):
    return Vector3(self.x - other.x , self.y - other.y , self.z - other.z)
  
  def __neg__(self):
    return Vector3( - self.x, - self.y, - self.z)
  
  def __str__(self) -> str:
    return '(' + str(self.x) +  ',' + str(self.y) +  ',' + str(self.z) + ')'

  def __lt__(self, other: 'Vector3'): 
    return self.x < other.x and self.y < other.y and self.z < other.z

  def __gt__(self, other: 'Vector3'): 
    return self.x > other.x and self.y > other.y and self.z > other.z

  def sig(self):
    return Vector3( sig(self.x), sig(self.y), sig(self.z))

  def Zero ():
    return Vector3(0,0,0)

  
  # retorn auna instanci ad ela clase donde sus componenetes 
  # x , y , z tienen un valor entre 0 y el paramentro max 
  def random(max: int):
    return Vector3( random.randint(0,max),
                    random.randint(0,max),
                    random.randint(0,max))


def sig (x : int):
  if x > 0: return 1 
  elif x < 0: return -1 
  else: return 0