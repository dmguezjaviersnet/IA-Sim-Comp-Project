from typing import Callable, Dict, Tuple
from orbsim_simulation_entities.orbsim_agent import OrbsimAgent
from orbsim_simulation_entities.point import Point

class SpaceDebrisCollector(OrbsimAgent):
	def __init__(self, container: Tuple[Point, Point], mass: float, volume: float, name: str, behaviour: Dict[str, Callable],
		speed: Point, life_span: float, fuel: float, capacity: float):
		super().__init__(container, mass, volume, behaviour, speed, name)
		self.life_span = life_span
		self.capacity = capacity
		self.fuel = fuel

	def scan(self):
		pass

	def __str__(self) -> str:
		return f'''space debris collector {self.name} with volume {self.volume} and mass 
		  {self.mass} located at {self.position}. Current life span is {self.life_span}.
		  Remaining fuel {self.fuel} and remaining capacity {self.capacity} //\\\\//'''
