import simpy
from typing import Tuple
from orbsim_simulation_entities.point import Point

# Esta clase me representa un objeto de la simulacion, es la clase
# mas "abstracta" de la representacion de los objetos del environment 

class OrbsimObj:
	def __init__(self, container: Tuple[Point, Point], mass: float, speed: Point, name: str, orientation_vector=(1, 1)):
		self.top_left = container[0]
		self.bottom_right = container[1]
		self.mass = mass
		self.speed = speed
		self.orientation_x = orientation_vector[0]
		self.orientation_y = orientation_vector[1]
		self.name = name
