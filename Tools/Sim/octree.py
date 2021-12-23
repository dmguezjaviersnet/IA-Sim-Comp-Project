
from typing import List


class Node:
  def __init__(self, region, objects):
    self.objects = objects
    self.region = region
    self.childs = []
    self.parent = None

class Objects:
  def __init__(self, mass, position, radius= 1):
    self.mass = mass
    self.position = position
    self.radius = radius




class Octree:
  def __init__(self, objects):
    self.root = Node(objects)

  def BuildTree(self, node: Node, objects: List[Objects]):
    for obj in objects:
