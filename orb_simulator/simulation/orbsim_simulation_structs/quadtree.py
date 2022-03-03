from enum import Enum, IntEnum
from typing import Tuple, List

from simulation.orbsim_simulation_entities import Point
from sprites_and_graph_ent.orbit_obj import OrbitObj
from sprites_and_graph_ent.space_agent import SpaceAgent
from sprites_and_graph_ent.space_debris import SpaceDebris
from sprites_and_graph_ent.satellite import Satellite
import pygame.draw
from sprites_and_graph_ent.space_obj import SpaceObj
from tools import RED_COLOR, WHITE_COLOR, WINE_COLOR


MAX_DEPTH = 8
MAX_LIMIT = 3

quadtree_pygame_window = None
low_depth_leave = None
collisions = []
# class LineColor(Enum):
# 	WHITE = (255, 255, 255)
# 	GREEN = (0, 255, 0)
# 	BLACK = (0, 0, 0)
# 	RED = (255, 0, 0)
# 	BLUE = (0, 0, 255)

class Child(IntEnum):
    NW = 0
    NE = 1
    SW = 2
    SE = 3

class Direction(Enum):
    NW = 0
    NE = 1
    SW = 2
    SE = 3
    N = 4
    S = 5
    W = 6
    E = 7

def detect_overlap(rect1_tl: Tuple[int, int], rect1_br: Tuple[int, int], rect2_tl: Tuple[int, int], rect2_br: Tuple[int, int]) -> bool:
	if (rect1_tl[0] < rect2_br[0] and rect1_tl[1] < rect2_br[1]
		and rect1_br[0] > rect2_tl[0] and rect1_br[1] > rect2_tl[1]):
		return True

	return False

def detect_collision(rect1_tl: Tuple[int, int], rect1_br: Tuple[int, int], rect2_tl: Tuple[int, int], rect2_br: Tuple[int, int]) -> bool:
	if (rect1_tl[0] <= rect2_br[0] and rect1_tl[1] <= rect2_br[1]
		and rect1_br[0] >= rect2_tl[0] and rect1_br[1] >= rect2_tl[1]):
		return True

	return False

def detect_full_overlap(rect1_tl: Tuple[int, int], rect1_br: Tuple[int, int], rect2_tl: Tuple[int, int], rect2_br: Tuple[int, int]) -> bool:
	if (rect1_tl[0] <= rect2_tl[0] and rect1_tl[1] <= rect2_tl[1]
		and rect1_br[0] >= rect2_br[0] and rect1_br[1] >= rect2_br[1]):
		return True

	return False

def draw_quadtree_line(color, point1, point2):
	global quadtree_pygame_window
	pygame.draw.line(quadtree_pygame_window, color, point1, point2)

class QuadTree:
	def __init__(self, screen, bounding_box: Tuple[Point, Point], qnode_lines):
		self.root = QTNode(None, bounding_box, 0, qnode_lines)
		self.collisions = 0
		global quadtree_pygame_window
		quadtree_pygame_window = screen
	
	def insert(self, obj: OrbitObj):
		self.root.insert(obj)

	def find_collisions(self):
		self.find_collisions()

class QTNode:
	def __init__(self, parent: 'QTNode', bounding_box: Tuple[Point, Point], depth, qnode_lines):
		self.parent = parent
		self.bounding_box_tl = (bounding_box[0].x, bounding_box[0].y)
		self.bounding_box_br = (bounding_box[1].x, bounding_box[1].y)
		self.depth = depth
		self.children: List[QTNode] = []
		self.objects: List[SpaceObj] = []
		self.neighbors: List[QTNode] = []
		self.center_x = ((bounding_box[0].x + bounding_box[1].x) / 2)
		self.center_y = ((bounding_box[0].y + bounding_box[1].y) / 2)
		self.qnode_lines = qnode_lines
		self.id = id(self)
	
	def __is_empty(self):
		return not self.objects

	def __is_leaf(self):
		return not self.children

	def __hash__(self):
		return self.id
		
	def split(self):
		q1 = QTNode(self, (Point(self.bounding_box_tl[0], self.bounding_box_tl[1]), Point(self.center_x, self.center_y)), self.depth + 1, self.qnode_lines)
		q2 = QTNode(self, (Point(self.center_x, self.bounding_box_tl[1]), Point(self.bounding_box_br[0], self.center_y)), self.depth + 1,self.qnode_lines)
		q3 = QTNode(self, (Point(self.bounding_box_tl[0], self.center_y), Point(self.center_x, self.bounding_box_br[1])), self.depth + 1, self.qnode_lines)
		q4 = QTNode(self, (Point(self.center_x, self.center_y), Point(self.bounding_box_br[0], self.bounding_box_br[1])), self.depth + 1, self.qnode_lines)
		
		if self.qnode_lines:
			draw_quadtree_line(RED_COLOR, (self.center_x, self.bounding_box_tl[1]), (self.center_x, self.bounding_box_br[1]))
			draw_quadtree_line(RED_COLOR, (self.bounding_box_tl[0], self.center_y), (self.bounding_box_br[0], self.center_y))

		for object in self.objects:
			if detect_overlap(object.rect.topleft, object.rect.bottomright, q1.bounding_box_tl, q1.bounding_box_br):
				q1.insert(object)
			if detect_overlap(object.rect.topleft, object.rect.bottomright,  q2.bounding_box_tl, q2.bounding_box_br):
				q2.insert(object)
			if detect_overlap(object.rect.topleft, object.rect.bottomright,  q3.bounding_box_tl, q3.bounding_box_br):
				q3.insert(object)
			if detect_overlap(object.rect.topleft, object.rect.bottomright,  q4.bounding_box_tl, q4.bounding_box_br):
				q4.insert(object)

		self.children = [q1 ,q2 ,q3 ,q4]
		self.objects.clear()

	def find(self, object: SpaceDebris) -> List['QTNode']:
		if (self.__is_leaf()): # invariant: if its a leaf, it has to be present in bounding box
			return [self]
		
		overlapping_leaves = []
		for i in range(4):
			q_node = self.children[i]
			if (detect_overlap(object.rect.topleft, object.rect.bottomright, q_node.bounding_box_tl, q_node.bounding_box_br)):
				if (q_node.__is_leaf()):
					overlapping_leaves.append(q_node)
				
				else: overlapping_leaves += q_node.find(object)
				
		return overlapping_leaves
	
	def insert(self, object: SpaceObj):
		for q_node in self.find(object):
			if (q_node.__is_leaf()):
				q_node.objects.append(object)
				if not detect_full_overlap(object.rect.topleft, object.rect.bottomright, q_node.bounding_box_tl, q_node.bounding_box_br):
					if q_node.depth < MAX_DEPTH:
						q_node.split()

					else:
						if isinstance(object, SpaceAgent):
							object.beliefs = q_node

	def check_collisions(self):
		for i, _ in enumerate(self.objects):
			j = i + 1
			while j < len(self.objects):
				if detect_collision(self.objects[i].rect.topleft, self.objects[i].rect.bottomright, 
									self.objects[j].rect.topleft, self.objects[j].rect.bottomright):
				
					self.objects[i].is_colliding = True
					self.objects[j].is_colliding = True
					if (isinstance(self.objects[i], SpaceDebris) and isinstance(self.objects[j], SpaceDebris) 
						or isinstance(self.objects[i], Satellite)  and isinstance(self.objects[j], SpaceDebris)
						or isinstance(self.objects[i], SpaceDebris)  and isinstance(self.objects[j], Satellite)):
						collisions.append((self.objects[i], self.objects[j]))

				j += 1
	
	def find_ge_size_neighbor(self, direction: Direction) -> 'QTNode':
        # Dirección Norte
		if direction == Direction.N:
			if self.parent is None:
				return None
			if self.parent.children[Child.SW] == self:
				return self.parent.children[Child.NW]
			if self.parent.children[Child.SE] == self:
				return self.parent.children[Child.NE]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

			return (node.children[Child.SW]
                    if self.parent.children[Child.NW] == self
                    else node.children[Child.SE])

        # Dirección Sur
		elif direction == Direction.S:
			if self.parent is None:
				return None
			if self.parent.children[Child.NW] == self:
				return self.parent.children[Child.SW]
			if self.parent.children[Child.NE] == self:
				return self.parent.children[Child.SE]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

            # 'self' is guaranteed to be a south child
			return (node.children[Child.NW]
                    if self.parent.children[Child.SW] == self
                    else node.children[Child.NE])

        # Dirección Oeste
		elif direction == Direction.W:
			if self.parent is None:
				return None
			if self.parent.children[Child.NE] == self:
				return self.parent.children[Child.NW]
			if self.parent.children[Child.SE] == self:
				return self.parent.children[Child.SW]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

            # 'self' is guaranteed to be a west child
			return (node.children[Child.NE]
                    if self.parent.children[Child.NW] == self
                    else node.children[Child.SE])

        # Dirección Este
		elif direction == Direction.E:
			if self.parent is None:
				return None
			if self.parent.children[Child.NW] == self:
				return self.parent.children[Child.NE]
			if self.parent.children[Child.SW] == self:
				return self.parent.children[Child.SE]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

            # 'self' is guaranteed to be an east child
			return (node.children[Child.NW]
                    if self.parent.children[Child.NE] == self
                    else node.children[Child.SW])

        # Dirección Noreste
		elif direction == Direction.NE:
			if self.parent is None:
				return None
			if self.parent.children[Child.SW] == self:
				return self.parent.children[Child.NE]
            
			direction = (direction if self.parent.children[Child.NE] == self
						else Direction.E if self.parent.children[Child.SE] == self
						else Direction.N)

			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node
                                    
			return (node.children[Child.SE]
                    if self.parent.children[Child.NW] == self
                    else node.children[Child.SW] if self.parent.children[Child.NE] == self
                    else node.children[Child.NW])

        # Dirección Noroeste
		elif direction == Direction.NW:
			if self.parent is None:
				return None
			if self.parent.children[Child.SE] == self:
				return self.parent.children[Child.NW]
            
			direction = (direction if self.parent.children[Child.NW] == self
						else Direction.W if self.parent.children[Child.SW] == self
						else Direction.N)

			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

			return (node.children[Child.SW]
                    if self.parent.children[Child.NE] == self
                    else node.children[Child.SE] if self.parent.children[Child.NW] == self
                    else node.children[Child.NE])

        # Dirección Sureste
		elif direction == Direction.SE:
			if self.parent is None:
				return None
			if self.parent.children[Child.NW] == self:
				return self.parent.children[Child.SE]
            
			direction = (direction if self.parent.children[Child.SE] == self
						else Direction.E if self.parent.children[Child.NE] == self
						else Direction.S)

			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

			return (node.children[Child.SW]
                    if self.parent.children[Child.NE] == self
                    else node.children[Child.NW] if self.parent.children[Child.SE] == self
                    else node.children[Child.NE])

        # Dirección Suroeste
		elif direction == Direction.SW:
			if self.parent is None:
				return None
			if self.parent.children[Child.NE] == self:
				return self.parent.children[Child.SW]
            
			direction = (direction if self.parent.children[Child.SW] == self
						else Direction.W if self.parent.children[Child.NW] == self
						else Direction.S)

			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

			return (node.children[Child.NW]
                    if self.parent.children[Child.SE] == self
                    else node.children[Child.NE] if self.parent.children[Child.SW] == self
                    else node.children[Child.SE])

	def find_smaller_size_neighbors(self, neighbor: 'QTNode', direction: Direction) -> List['QuadTree']:   
		candidates = [] if not neighbor else [neighbor]
		neighbors = []
    
        # Dirección Norte
		if direction == Direction.N:
			while candidates:
				curr_candidate = candidates.pop(0)
				if curr_candidate.__is_leaf():
					neighbors.append(curr_candidate)

				else:
					candidates.append(curr_candidate.children[Child.SW])
					candidates.append(curr_candidate.children[Child.SE])
                    
			return neighbors

        # Dirección Sur
		elif direction == Direction.S:
			while candidates:
				curr_candidate = candidates.pop(0)
				if curr_candidate.__is_leaf():
					neighbors.append(curr_candidate)

				else:
					candidates.append(curr_candidate.children[Child.NW])
					candidates.append(curr_candidate.children[Child.NE])

			return neighbors

        # Dirección Este
		elif direction == Direction.E:
			while candidates:
				curr_candidate = candidates.pop(0)
				if curr_candidate.__is_leaf():
					neighbors.append(curr_candidate)

				else:
					candidates.append(curr_candidate.children[Child.SW])
					candidates.append(curr_candidate.children[Child.NW])

			return neighbors

        # Dirección Oeste
		elif direction == Direction.W:
			while candidates:
				curr_candidate = candidates.pop(0)
				if curr_candidate.__is_leaf():
					neighbors.append(curr_candidate)

				else:
					candidates.append(curr_candidate.children[Child.SE])
					candidates.append(curr_candidate.children[Child.NE])

			return neighbors

        # Dirección Noreste
		elif direction == Direction.NE:
			while candidates:
				curr_candidate = candidates.pop(0)
				if curr_candidate.__is_leaf():
					neighbors.append(curr_candidate)

				else:
					candidates.append(curr_candidate.children[Child.SW])
                    
			return neighbors

        # Dirección Noroeste
		elif direction == Direction.NW:
			while candidates:
				curr_candidate = candidates.pop(0)
				if curr_candidate.__is_leaf():
					neighbors.append(curr_candidate)

				else:
					candidates.append(curr_candidate.children[Child.SE])

			return neighbors
        
        # Dirección Sureste
		elif direction == Direction.SE:
			while candidates:
				curr_candidate = candidates.pop(0)
				if curr_candidate.__is_leaf():
					neighbors.append(curr_candidate)

				else:
					candidates.append(curr_candidate.children[Child.NW])
                    
			return neighbors
        
        # Dirección Suroreste
		elif direction == Direction.SW:
			while candidates:
				curr_candidate = candidates.pop(0)
				if curr_candidate.__is_leaf():
					neighbors.append(curr_candidate)

				else:
					candidates.append(curr_candidate.children[Child.NE])

			return neighbors
            
	def find_neighbors(self):
		all_neighbors = []
		for direction in Direction:
			neighbor = self.find_ge_size_neighbor(direction)
			all_neighbors += self.find_smaller_size_neighbors(neighbor, direction)

		self.neighbors = all_neighbors

		# for neigh in self.neighbors:
		# 	for obj in neigh.objects:
		# 		obj.image.fill(WINE_COLOR)