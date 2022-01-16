from typing import *


class vector2:
  def __init__(self, x: int , y: int ) -> None:
    self.x = x 
    self.y = y

  def __add__ (self, other):
    return vector2(self.x + other.x , self.y + other.y)

  def __sub__ (self, other):
    return vector2(self.x - other.x, self.y - other.y)

  def __mul__ (self, other):
    return vector2(self.x * other.x, self.y * other.y)
  
  def __div__ (self, other):
    return vector2(self.x / other.x, self.y / other.y)

  def zero():
    return vector2(0, 0)