from typing import List
from orbsim_simulation_entities.point import Point

class Vertex:

	def __init__(self, coordinates: Point):
		self.coordinates = coordinates
		self.neighbors: List[Vertex] = []