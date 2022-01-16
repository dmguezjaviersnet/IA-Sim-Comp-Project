from typing import * 

class Vector3:
  def __init__(self, x:int , y:int, z:int) -> None:
    self.x: int = x 
    self.y: int = y
    self.z: int = z
    self.lst:List[int] = [x,y,z] 
  
  def __add__ (self , other):
    return Vector3(self.x + other.x , self.y + other.y , self.z + other.z)
  
  def __sub__ (self , other):
    return Vector3(self.x - other.x , self.y - other.y , self.z - other.z)
  
  def __neg__(self):
    return Vector3( - self.x, - self.y, - self.z)
  
  def __str__(self) -> str:
    return '(' + str(self.x) +  ',' + str(self.y) +  ',' + str(self.z) + ')'

  def sig(self):
    return Vector3( sig(self.x), sig(self.y), sig(self.z))

def sig (x : int):
  if x > 0: return 1 
  if x < 0: return -1 
  else: return 0 

