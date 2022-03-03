import heapq
import math
from random import randint
from math import dist
from typing import Dict, List, Tuple
from simulation.orbsim_simulation_structs.quadtree import QTNode
from sprites_and_graph_ent.satellite import Satellite
from sprites_and_graph_ent.space_agent import SpaceAgent, AgentActionData
from simulation.a_star import a_star, eucl_dist_qtnode
from sys import maxsize
import random
from sprites_and_graph_ent.space_debris import SpaceDebris

MOVE_RANDOMLY = 'move randomly to empty space'
MOVE_TOWARDS_DEBRIS = 'move towards debris'
BECOME_DEBRIS = 'become debris'
COLLECT_DEBRIS = 'collect debris'
MOVE_TO_SATELLITE = 'move to satellite'
IDLE = 'idle'

class SpaceDebrisCollector(SpaceAgent):

	def __init__(self, pos_x: int, pos_y: int, life_span: int, capacity: int, fuel: int, vel = 10):
		super().__init__(pos_x, pos_y, 8)
		self.life_span = life_span
		self.capacity = capacity
		self.fuel = fuel
		self.collected_debris = []
		self.vel = vel
		self.action_target: AgentActionData = AgentActionData(-1, None, None, IDLE)
		self.path_to_target: List = []
		self.qt_node_target: QTNode = None

	def options(self):
		if self.desires:
			self.desires.clear()
		visited: List[QTNode] = []
		possible_random_moves = []

		perceived_env = [(self.beliefs, 0)]
		self.desires = []

		if self.life_span:
			while(perceived_env):
				curr_env, at_range = perceived_env.pop(0)
				if at_range < self.perception_range:
					for qt_node in curr_env.neighbors:
						if qt_node not in visited:
							visited.append(qt_node)
							self_object = False
							if qt_node.objects:
								for object in qt_node.objects:
									if object != self:
										if isinstance(object, SpaceDebris):
											if object.area < self.capacity:
												distance = dist((self.pos_x, self.pos_y), object.rect.center)
												if self.fuel*5 >= distance:
													heapq.heappush(self.desires, AgentActionData(distance, qt_node, object, 
																COLLECT_DEBRIS if at_range == 0 else MOVE_TOWARDS_DEBRIS))
											
										elif isinstance(object, Satellite):
											heapq.heappush(self.desires, AgentActionData(distance, qt_node, object, MOVE_TO_SATELLITE))

									else:
										self_object = True 
										perceived_env.append((qt_node, 0))

							else: possible_random_moves.append(qt_node)

							if not self_object:
								perceived_env.append((qt_node, at_range + 1))
				
		if not self.desires:
			if self.fuel and self.life_span:
				random_move = randint(0, len(possible_random_moves) - 1)
				# print(f'random_move to {random_move}')
				heapq.heappush(self.desires, AgentActionData(None, possible_random_moves[random_move], None, MOVE_RANDOMLY))
			
			else:
				heapq.heappush(self.desires, AgentActionData(None, self.beliefs.neighbors[random_move], None, BECOME_DEBRIS))
		
		top_priority_target: 'AgentActionData' = heapq.heappop(self.desires)

		if self.action_target.action == IDLE:
			self.action_target = top_priority_target
			self.pursue_goal()

		elif top_priority_target.best_action_to_change(self.action_target):
			self.action_target = top_priority_target
			self.pursue_goal()

	def pursue_goal(self):
		if self.action_target.action == MOVE_RANDOMLY or self.action_target.action ==  MOVE_TOWARDS_DEBRIS:
			self.path_to_target = a_star(self.beliefs, self, eucl_dist_qtnode, self.action_target.qt_node)
			self.qt_node_target = self.path_to_target.pop(0)
		
		elif self.action_target.action == COLLECT_DEBRIS:
			self.capacity -= self.action_target.object.area
			self.fuel -= self.action_target.object.area/2
			self.collected_debris.append(self.action_target.object)
			self.action_target = AgentActionData(-1, None, None, IDLE)

		elif self.action_target.action == BECOME_DEBRIS:
			self.action_target = AgentActionData(-1, None, None, IDLE)
			return self
	
	def update(self):
		if (self.action_target and (self.action_target.action == MOVE_TOWARDS_DEBRIS or self.action_target.action == MOVE_RANDOMLY)):
			diff_x = self.qt_node_target.center_x - self.pos_x
			diff_y = self.qt_node_target.center_y - self.pos_y
			norm = dist(((self.pos_x), (self.pos_y)), (self.qt_node_target.center_x, self.qt_node_target.center_y))

			if norm:
				normalize = (diff_x/round(norm), diff_y/round(norm))
				
				speed = (round(normalize[0]*self.vel), round(normalize[1]*self.vel))
				new_pos_x = self.pos_x + speed[0] if abs(speed[0]) < abs(diff_x) else self.qt_node_target.center_x
				new_pos_y = self.pos_y + speed[1] if abs(speed[1]) < abs(diff_y) else self.qt_node_target.center_y
				
				dist_traveled = dist((new_pos_x, new_pos_y), (self.pos_x, self.pos_y))
				self.fuel -= dist_traveled/5
				self.rect.center = [new_pos_x, new_pos_y]

			else:
				if self.path_to_target:
					self.qt_node_target = self.path_to_target.pop(0)
				
				else: self.action_target = AgentActionData(-1, None, None, IDLE)
					



		


		


