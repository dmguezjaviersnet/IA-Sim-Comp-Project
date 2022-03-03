from abc import abstractmethod
import heapq
from typing import Any, List
from sprites_and_graph_ent.satellite import Satellite
from sprites_and_graph_ent.space_debris import SpaceDebris
from sprites_and_graph_ent.space_obj import SpaceObj
import pygame
from tools import LIGHT_GRAY

MOVE_RANDOMLY = 'move randomly to empty space'
MOVE_TOWARDS_DEBRIS = 'move towards debris'
BECOME_DEBRIS = 'become debris'
COLLECT_DEBRIS = 'collect debris'
MOVE_TO_SATELLITE = 'move to satellite'
IDLE = 'idle'
class AgentActionData:

	def __init__(self, distance: int, qt_node, object: SpaceDebris, action: str) -> None:
		self.distance = distance
		self.qt_node = qt_node
		self.object = object
		self.action = action
		
	def __lt__(self, other: 'AgentActionData'):
		if self.action == 'become debris':
			return True

		if self.action == 'collect debris':
			if other.action == 'collect debris':
				return (self.distance < other.distance if self.object.area == other.object.area
						else self.object.area < other.object.area)

			if other.action == 'move towards debris':
				return self.object.area <= other.object.area

			return True
		
		if self.action == 'move towards debris':
			if other.action == 'collect debris':
				return self.object.area < other.object.area

			if other.action == 'move towards debris':
				return (self.distance < other.distance if self.object.area == other.object.area
						else self.object.area < other.object.area)

			return True

		if self.action == 'move randomly to empty space':
			if other.action == 'move randomly to empty space':
				return False
			
			if other.action == 'move to satellite':
				return True

			return False
		
		if self.action == 'move to satellite':
			if other.action == 'move to satellite':
				return True
			
			return False

	def best_action_to_change(self, other_action: 'AgentActionData'):
		if self.action == MOVE_TOWARDS_DEBRIS and other_action.action != MOVE_TOWARDS_DEBRIS and other_action.action != COLLECT_DEBRIS:
			return True

		if self.action == COLLECT_DEBRIS and other_action.action != COLLECT_DEBRIS:
			return True
			
		return False

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