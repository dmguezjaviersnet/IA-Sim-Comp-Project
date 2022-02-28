from abc import abstractmethod
import heapq
from typing import Any, List
from simulation.orbsim_simulation_structs.agent_action_data import AgentActionData
from simulation.orbsim_simulation_structs.quadtree import QTNode, QuadTree
from sprites_and_graph_ent.space_obj import SpaceObj
import pygame
class SpaceAgent(SpaceObj):
	
	def __init__(self, pos_x: int, pos_y: int, perception_range: int):
		super().__init__()
		self.beliefs: QTNode = None
		self.desires: heapq[AgentActionData] = None
		self.intentions: AgentActionData = None
		self.size = (35,35)
		self.image = pygame.Surface([self.size[0], self.size[1]])
		self.rect = self.image.get_rect()
		self.rect.center = [pos_x, pos_y]
		self.image.set_colorkey((255, 0, 255))
		# self.pos_x = pos_x
		# self.pos_y = pos_y
		self.perception_range = perception_range

	@property
	def pos(self):
		return self.rect.center
	
	@property
	def pos_x(self):
		return self.rect.center[0]
	
	@property
	def pos_y(self):
		return self.rect.center[1]
	
	def scan(self, environment: QuadTree):
		environment.insert(self)
    
	@abstractmethod
	def options(self):
		...

	@abstractmethod
	def pursue_goal(self):
		...