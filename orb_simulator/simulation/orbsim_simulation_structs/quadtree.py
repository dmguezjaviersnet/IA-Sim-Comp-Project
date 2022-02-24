from enum import Enum, IntEnum
from typing import Tuple, List
from xml.etree.ElementTree import QName
from simulation.orbsim_simulation_entities import OrbsimObj, Point
from sprites_and_graph_ent.space_debris import SpaceDebris
import pygame.draw
from tools import RED_COLOR


MAX_DEPTH = 8
MAX_LIMIT = 3

quadtree_pygame_window = None
leaves: List['QTNode'] = []

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


class QTNode:
	def __init__(self, parent: 'QTNode', bounding_box: Tuple[Point, Point], depth):
		self.parent = parent
		self.bounding_box_tl = (bounding_box[0].x, bounding_box[0].y)
		self.bounding_box_br = (bounding_box[1].x, bounding_box[1].y)
		self.depth = depth
		self.children: List[QTNode] = []
		self.objects: List[SpaceDebris] = []
		self.center_x = ((bounding_box[0].x + bounding_box[1].x) / 2)
		self.center_y = ((bounding_box[0].y + bounding_box[1].y) / 2)
	
	def __is_empty(self):
		return not self.objects

	# returns true if a node is a leaf in the quadtree
	def __is_leaf(self):
		return not self.children

	def split(self):
		# if (self.__is_empty()):
		# 	return

		q1 = QTNode(self, (Point(self.bounding_box_tl[0], self.bounding_box_tl[1]), Point(self.center_x, self.center_y)), self.depth + 1)
		q2 = QTNode(self, (Point(self.center_x, self.bounding_box_tl[1]), Point(self.bounding_box_br[0], self.center_y)), self.depth + 1)
		q3 = QTNode(self, (Point(self.bounding_box_tl[0], self.center_y), Point(self.center_x, self.bounding_box_br[1])), self.depth + 1)
		q4 = QTNode(self, (Point(self.center_x, self.center_y), Point(self.bounding_box_br[0], self.bounding_box_br[1])), self.depth + 1)

		draw_quadtree_line(RED_COLOR, (self.center_x, self.bounding_box_tl[1]), (self.center_x, self.bounding_box_br[1]))
		draw_quadtree_line(RED_COLOR, (self.bounding_box_tl[0], self.center_y), (self.bounding_box_br[0], self.center_y))

		# assert len(self.objects) > MAX_LIMIT
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
		self.objects = None

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
	
	# inserts a point into the quadtree
	def insert(self, object: SpaceDebris):
		# if (not detect_overlap((object.top_left, object.bottom_right), self.boundingBox)):
		# 	return

		for q_node in self.find(object):
			if (q_node.__is_leaf()):
				q_node.objects.append(object)
				if not detect_full_overlap(object.rect.topleft, object.rect.bottomright, q_node.bounding_box_tl, q_node.bounding_box_br):
					if  q_node.depth < MAX_DEPTH:
						q_node.split()

					else: leaves.append(q_node)

	# splits current quad tree into 4 smaller quad trees
	# Method to detect collisions for the quadtree built for the frame
	def check_collisions(self):
		# a leaf can contain maximum maxLimit # of objects. So, an n^2 approach here is ok
		for i, _ in enumerate(self.objects):
			j = i + 1
			while j < len(self.objects):
				if detect_collision(self.objects[i].rect.topleft, self.objects[i].rect.bottomright, 
									self.objects[j].rect.topleft, self.objects[j].rect.bottomright):

					self.objects[i].is_colliding = True
					self.objects[j].is_colliding = True

				j += 1
	
	def find_ge_size_neighbor(self, direction: Direction) -> 'QTNode':
        # Dirección Norte
		if direction == Direction.N:
			if self.parent is None:
				return None
			if self.parent.children[Child.SW] == self: # Is 'self' SW child?
				return self.parent.children[Child.NW]
			if self.parent.children[Child.SE] == self: # Is 'self' SE child?
				return self.parent.children[Child.NE]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

            # 'self' is guaranteed to be a north child
			return (node.children[Child.SW]
                    if self.parent.children[Child.NW] == self # Is 'self' NW child?
                    else node.children[Child.SE])

        # Dirección Sur
		elif direction == Direction.S:
			if self.parent is None:
				return None
			if self.parent.children[Child.NW] == self: # Is 'self' NW child?
				return self.parent.children[Child.SW]
			if self.parent.children[Child.NE] == self: # Is 'self' NE child?
				return self.parent.children[Child.SE]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

            # 'self' is guaranteed to be a south child
			return (node.children[Child.NW]
                    if self.parent.children[Child.SW] == self # Is 'self' SW child?
                    else node.children[Child.NE])

        # Dirección Oeste
		elif direction == Direction.W:
			if self.parent is None:
				return None
			if self.parent.children[Child.NE] == self: # Is 'self' NE child?
				return self.parent.children[Child.NW]
			if self.parent.children[Child.SE] == self: # Is 'self' SE child?
				return self.parent.children[Child.SW]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

            # 'self' is guaranteed to be a west child
			return (node.children[Child.NE]
                    if self.parent.children[Child.NW] == self # Is 'self' SW child?
                    else node.children[Child.SE])

        # Dirección Este
		elif direction == Direction.E:
			if self.parent is None:
				return None
			if self.parent.children[Child.NW] == self: # Is 'self' NW child?
				return self.parent.children[Child.NE]
			if self.parent.children[Child.SW] == self: # Is 'self' SW child?
				return self.parent.children[Child.SE]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

            # 'self' is guaranteed to be an east child
			return (node.children[Child.NW]
                    if self.parent.children[Child.NE] == self # Is 'self' SW child?
                    else node.children[Child.SW])

        # Dirección Noreste
		elif direction == Direction.NE:
			if self.parent is None:
				return None
			if self.parent.children[Child.SW] == self: # Is 'self' SW child?
				return self.parent.children[Child.NE]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

			return (node.children[Child.SE]
                    if self.parent.children[Child.NW] == self # Is 'self' SW child?
                    else node.children[Child.SW] if self.parent.children[Child.NE] == self
                    else node.children[Child.NW])

        # Dirección Noroeste
		elif direction == Direction.NW:
			if self.parent is None:
				return None
			if self.parent.children[Child.SE] == self: # Is 'self' SE child?
				return self.parent.children[Child.NW]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

			return (node.children[Child.SW]
                    if self.parent.children[Child.NE] == self # Is 'self' SW child?
                    else node.children[Child.SE] if self.parent.children[Child.NW] == self
                    else node.children[Child.NE])

        # Dirección Sureste
		elif direction == Direction.SE:
			if self.parent is None:
				return None
			if self.parent.children[Child.NW] == self: # Is 'self' NW child?
				return self.parent.children[Child.SE]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

			return (node.children[Child.SW]
                    if self.parent.children[Child.NE] == self # Is 'self' SW child?
                    else node.children[Child.NW] if self.parent.children[Child.SE] == self
                    else node.children[Child.NE])

        # Dirección Suroeste
		elif direction == Direction.SW:
			if self.parent is None:
				return None
			if self.parent.children[Child.NE] == self: # Is 'self' NE child?
				return self.parent.children[Child.SW]
                
			node = self.parent.find_ge_size_neighbor(direction)
			if node is None or node.__is_leaf():
				return node

			return (node.children[Child.NW]
                    if self.parent.children[Child.SE] == self # Is 'self' SW child?
                    else node.children[Child.NE] if self.parent.children[Child.SW] == self
                    else node.children[Child.SE])

            # TODO: implement other directions symmetric to NORTH case
			# assert False
			# return []

	def find_smaller_size_neighbors(self, neighbor: 'QTNode', direction: Direction) -> List['QuadTree']:   
		candidates = [] if not neighbor else [neighbor]
		neighbors = []
    
        # Dirección Norte
		if direction == Direction.N:
			while len(candidates) > 0:
				if candidates[0].__is_leaf():
					neighbors.append(candidates[0])
				else:
					candidates.append(candidates[0].children[Child.SW])
					candidates.append(candidates[0].children[Child.SE])
                    
				candidates.remove(candidates[0])

			return neighbors

        # Dirección Norte
		elif direction == Direction.S:
			while len(candidates) > 0:
				if candidates[0].__is_leaf():
					neighbors.append(candidates[0])
				else:
					candidates.append(candidates[0].children[Child.NW])
					candidates.append(candidates[0].children[Child.NE])
                    
				candidates.remove(candidates[0])

			return neighbors

        # Dirección Este
		elif direction == Direction.E:
			while len(candidates) > 0:
				if candidates[0].__is_leaf():
					neighbors.append(candidates[0])
				else:
					candidates.append(candidates[0].children[Child.SW])
					candidates.append(candidates[0].children[Child.NW])
                    
				candidates.remove(candidates[0])

			return neighbors

        # Dirección Oeste
		elif direction == Direction.W:
			while len(candidates) > 0:
				if candidates[0].__is_leaf():
					neighbors.append(candidates[0])
				else:
					candidates.append(candidates[0].children[Child.SE])
					candidates.append(candidates[0].children[Child.NE])
                    
				candidates.remove(candidates[0])

			return neighbors

        # Dirección Noreste
		elif direction == Direction.NE:
			while len(candidates) > 0:
				if candidates[0].__is_leaf():
					neighbors.append(candidates[0])
				else:
					candidates.append(candidates[0].children[Child.SW])
                    
				candidates.remove(candidates[0])

			return neighbors

        # Dirección Noroeste
		elif direction == Direction.NW:
			while len(candidates) > 0:
				if candidates[0].__is_leaf():
					neighbors.append(candidates[0])
				else:
					candidates.append(candidates[0].children[Child.SE])
                    
				candidates.remove(candidates[0])

			return neighbors
        
        # Dirección Sureste
		elif direction == Direction.SE:
			while len(candidates) > 0:
				if candidates[0].__is_leaf():
					neighbors.append(candidates[0])
				else:
					candidates.append(candidates[0].children[Child.NW])
                    
				candidates.remove(candidates[0])

			return neighbors
        
        # Dirección Suroreste
		elif direction == Direction.SW:
			while len(candidates) > 0:
				if candidates[0].__is_leaf():
					neighbors.append(candidates[0])
				else:
					candidates.append(candidates[0].children[Child.NE])
                    
				candidates.remove(candidates[0])

			return neighbors

            # TODO: implement other directions symmetric to NORTH case
			assert False
            
	def find_neighbors(self) -> List['QTNode']:
		all_neighbors = []
		for direction in Direction:
			neighbor = self.find_ge_size_neighbor(direction)
			all_neighbors += self.find_smaller_size_neighbors(neighbor, direction)

		self.neighbors = all_neighbors

# Quad Tree data structure
class QuadTree:
	def __init__(self, screen, bounding_box: Tuple[Point, Point]):
		self.root = QTNode(None, bounding_box, 0)
		self.collisions = 0
		global quadtree_pygame_window
		quadtree_pygame_window = screen
	
	def insert(self, obj):
		self.root.insert(obj)

	def find_collisions(self):
		self.find_collisions()