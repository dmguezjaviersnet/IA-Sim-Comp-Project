from abc import abstractmethod
import heapq
from typing import Any, List
from simulation.orbsim_simulation_structs.agent_action_data import AgentActionData
from simulation.orbsim_simulation_structs.quadtree import QTNode, QuadTree
from sprites_and_graph_ent.space_obj import SpaceObj

class SpaceAgent(SpaceObj):
	
	def __init__(self, pos_x: int, pos_y: int, perception_range: int):
		super().__init__()
		self.beliefs: QTNode = None
		self.desires: heapq[AgentActionData] = None
		self.intentions: AgentActionData = None
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.perception_range = perception_range

	def scan(self, environment: QuadTree):
		environment.insert(self)
    
	@abstractmethod
	def options(self):
		...

	@abstractmethod
	def filter(self):
		...