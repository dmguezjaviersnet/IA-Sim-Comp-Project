import heapq
import math
from random import randint
from math import dist
from typing import Dict, List, Tuple
from simulation.orbsim_simulation_structs.quadtree import QTNode
from sprites_and_graph_ent.space_agent import SpaceAgent, AgentActionData
from simulation.a_star import a_star, eucl_dist_qtnode


class SpaceDebrisCollector(SpaceAgent):

	def __init__(self, pos_x: int, pos_y: int, life_span: int, capacity: int, fuel: int, vel_x = 1, vel_y = 1):
		super().__init__(pos_x, pos_y, 5)
		self.path_to_debris: List = None
		self.life_span = life_span
		self.capacity = capacity
		self.fuel = fuel
		self.vel_x = vel_x
		self.vel_y = vel_y

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
				curr_heur_val = 0
				for qt_node in curr_env.neighbors:
					if qt_node not in visited:
						visited.append(qt_node)
						self_object = False
						if qt_node.objects:
							for object in qt_node.objects:
								if object != self:
									if object.area < self.capacity:
										distance = dist((self.pos_x, self.pos_y), object.rect.center)
										if self.fuel*2 >= distance:
											curr_heur_val = object.area
											heapq.heappush(self.desires, AgentActionData(curr_heur_val, distance, qt_node, object, 
															'collect debris' if at_range == 0 else 'move towards debris'))

								else:
									self_object = True 
									perceived_env.append((qt_node, 0))
						
						else: possible_random_moves.append(qt_node)

						if not self_object:
							perceived_env.append((qt_node, at_range + 1))

				# if at_range < self.perception_range:
				# 	if not qt_node in visited:
				# 		perceived_env.append((qt_node, at_range))
				# 		visited[qt_node] = True
				
		if not self.desires:
			if self.fuel and self.life_span:
				random_move = randint(0, len(possible_random_moves) - 1)
				print(f'random_move to {random_move}')
				heapq.heappush(self.desires, AgentActionData(0, 0, possible_random_moves[random_move], None, 'move randomly'))
			
			else:
				heapq.heappush(self.desires, AgentActionData(0, 0, self.beliefs.neighbors[random_move], None, 'become debris'))
		
		self.intentions = heapq.heappop(self.desires)

	def pursue_goal(self):
		if self.intentions.action == 'move randomly':
			self.update()
		
		elif self.intentions.action == 'move towards debris':
			self.path_to_debris = a_star(self.beliefs, eucl_dist_qtnode, self.intentions.qt_node)
			self.intentionsrandom_move.qt_node = self.path_to_debris.pop(0)
			self.update()
			
		elif self.intentions.action == 'collect debris':
			self.capacity -= self.intentions.object.area
			self.fuel -= self.intentions.object.area/2
			return self.intentions.object
	
	def update(self):
		self.vel_x = self.pos_x - self.intentions.qt_node.center_x
		self.vel_y = self.pos_y - self.intentions.qt_node.center_y
		norm = dist((self.pos_x, self.pos_y), (self.intentions.qt_node.center_x, self.intentions.qt_node.center_y))

		self.vel_x = 0.4*self.vel_x/norm
		self.vel_y = 0.4*self.vel_y/norm

		new_pos_x = self.pos_x + self.vel_x
		new_pos_y = self.pos_y + self.vel_y

		dist_traveled = dist((new_pos_x, new_pos_y), (self.pos_x, self.intentions.qt_node.center_y))
		self.fuel -= dist_traveled/5
		self.rect.center = [new_pos_x, new_pos_y]
		


		


