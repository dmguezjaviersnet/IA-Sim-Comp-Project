from typing import Tuple
from orbsim_simulation_entities.orbsim_obj import OrbsimObj
from orbsim_simulation_entities.point import Point

class SpaceDebris(OrbsimObj):

	def __init__(self , container: Tuple[Point, Point], mass: float, speed: Point, name: str):
		super().__init__(container, mass, speed, name)
		self.integrity = 100

	def __hash__(self) -> int:
		return hash((self.position, self.mass, self.radius, self.name, self.integrity))

	def __str__(self) -> str:
		return f'''space debris {self.name} with radius {self.radius} and mass 
			{self.mass} located at {self.position}. Current life span is {self.integrity}% //\\\\//'''
