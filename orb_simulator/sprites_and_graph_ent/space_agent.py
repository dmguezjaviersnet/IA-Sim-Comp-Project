from abc import abstractmethod
import heapq
from typing import Any, List
from sprites_and_graph_ent.space_debris import SpaceDebris
from sprites_and_graph_ent.space_obj import SpaceObj
import pygame
from tools import LIGHT_GRAY
class AgentActionData:

    def __init__(self, area: int, distance: int, qt_node, object: SpaceDebris, action: str) -> None:
        self.area = area
        self.distance = distance
        self.qt_node = qt_node
        self.object = object
        self.action = action

    def __lt__(self, other: 'AgentActionData'):
        return True if self.area < other.area else self.distance < other.distance if self.area == other.area else False

class SpaceAgent(SpaceObj):
	
	def __init__(self, pos_x: int, pos_y: int, perception_range: int):
		super().__init__()
		self.beliefs = None
		self.desires: List = []
		self.intentions: AgentActionData = None
		self.size = (35,35)
		self.image = pygame.Surface([self.size[0], self.size[1]])
		self.image.fill(LIGHT_GRAY)
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
	
	def scan(self, environment):
		environment.insert(self)
    
	@abstractmethod
	def options(self):
		...

	@abstractmethod
	def pursue_goal(self):
		...