from typing import Callable, Dict, Tuple
from simulation.orbsim_simulation_entities.point import Point
from simulation.orbsim_simulation_entities.orbsim_obj import OrbsimObj

class OrbsimAgent(OrbsimObj): 
	def __init__(self, container: Tuple[Point, Point], mass: float, volume: float, behaviour: Dict[str, Callable], speed: Point, name: str) -> None:
		self.container = container
		self.mass = mass
		self.volume = volume
		self.behaviour = behaviour
		self.speed = speed
		self.name = name

	def __getattr__(self, index: str):
		return self.behaviour[index]