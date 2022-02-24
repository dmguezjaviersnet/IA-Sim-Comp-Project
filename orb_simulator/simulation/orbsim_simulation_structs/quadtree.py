from enum import Enum, IntEnum
from typing import Tuple, List
from simulation.orbsim_simulation_entities import OrbsimObj, Point
import pygame.draw

MAX_DEPTH = 6
MAX_LIMIT = 3

quadtree_pygame_window = None
leaves: List['QTNode'] = []

class LineColor(Enum):
	WHITE = (255, 255, 255)
	GREEN = (0, 255, 0)
	BLACK = (0, 0, 0)
	RED = (255, 0, 0)
	BLUE = (0, 0, 255)

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

def detect_overlap(rect1: Tuple[Point, Point], rect2: Tuple[Point, Point]) -> bool:
	if (rect1[0].x < rect2[1].x and rect1[0].y < rect2[1].y
		and rect1[1].x > rect2[0].x and rect1[1].y > rect2[0].y):
		return True

	return False

def detect_collision(rect1: Tuple[Point, Point], rect2: Tuple[Point, Point]) -> bool:
	if (rect1[0].x <= rect2[1].x and rect1[0].y <= rect2[1].y
		and rect1[1].x >= rect2[0].x and rect1[1].y >= rect2[0].y):
		return True

	return False

def detect_full_overlap(rect1: Tuple[Point, Point], rect2: Tuple[Point, Point]) -> bool:
	if (rect1[0].x <= rect2[0].x and rect1[0].y <= rect2[0].y
		and rect1[1].x >= rect2[1].x and rect1[1].y >= rect2[1].y):
		return True

	return False

def draw_quadtree_line(color, point1, point2):
	global quadtree_pygame_window
	pygame.draw.line(quadtree_pygame_window, color, point1, point2)


class QTNode:
	def __init__(self, parent: 'QTNode', bounding_box: Tuple[Point, Point], depth):
		self.parent = parent
		self.bounding_box = bounding_box # bounding box is a property of the QTree and not the QTNode
		self.depth = depth
		self.children: List[QTNode] = []
		self.objects: List[OrbsimObj] = []
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

		q1 = QTNode(self, (Point(self.bounding_box[0].x, self.bounding_box[0].y), Point(self.center_x, self.center_y)), self.depth + 1)
		q2 = QTNode(self, (Point(self.center_x, self.bounding_box[0].y), Point(self.bounding_box[1].x, self.center_y)), self.depth + 1)
		q3 = QTNode(self, (Point(self.bounding_box[0].x, self.center_y), Point(self.center_x, self.bounding_box[1].y)), self.depth + 1)
		q4 = QTNode(self, (Point(self.center_x, self.center_y), Point(self.bounding_box[1].x, self.bounding_box[1].y)), self.depth + 1)

		draw_quadtree_line(LineColor.RED.value, (self.center_x, self.bounding_box[0].y), (self.center_x, self.bounding_box[1].y))
		draw_quadtree_line(LineColor.RED.value, (self.bounding_box[0].x, self.center_y), (self.bounding_box[1].x, self.center_y))

		# assert len(self.objects) > MAX_LIMIT
		for object in self.objects:
			if (detect_overlap((object.top_left, object.bottom_right), q1.bounding_box)):
				q1.insert(object)
			if (detect_overlap((object.top_left, object.bottom_right), q2.bounding_box)):
				q2.insert(object)
			if (detect_overlap((object.top_left, object.bottom_right), q3.bounding_box)):
				q3.insert(object)
			if (detect_overlap((object.top_left, object.bottom_right), q4.bounding_box)):
				q4.insert(object)

		self.children = [q1 ,q2 ,q3 ,q4]
		self.objects = None

	def find(self, object: OrbsimObj) -> List['QTNode']:
		if (self.__is_leaf()): # invariant: if its a leaf, it has to be present in bounding box
			return [self]
		
		overlapping_leaves = []
		for i in range(4):
			q_node = self.children[i]
			if (detect_overlap((object.top_left, object.bottom_right), q_node.bounding_box)):
				if (q_node.__is_leaf()):
					overlapping_leaves.append(q_node)
				
				else: overlapping_leaves += q_node.find(object)
				
		return overlapping_leaves
	
	# inserts a point into the quadtree
	def insert(self, object: OrbsimObj):
		# if (not detect_overlap((object.top_left, object.bottom_right), self.boundingBox)):
		# 	return

		for q_node in self.find(object):
			if (q_node.__is_leaf()):
				q_node.objects.append(object)
				if not detect_full_overlap((object.top_left, object.bottom_right), q_node.bounding_box):
					if  q_node.depth < MAX_DEPTH:
						q_node.split()

					else: leaves.append(q_node)

	# splits current quad tree into 4 smaller quad trees
	# Method to detect collisions for the quadtree built for the frame
	def count_collisions(self):
		# dfs
		if (self.__is_empty()):
			return self.collisions

		if (self.__is_leaf()):
			# a leaf can contain maximum maxLimit # of objects. So, an n^2 approach here is ok
			i = 0
			objects_amount = len(self.objects)
			while (i < objects_amount):
				j = i + 1
				while (j < objects_amount):
					if (detect_collision(self.objects[i], self.objects[j])):
						# coord1 = (self.points[i].x, self.points[i].y)
						# coord2 = (self.points[j].x, self.points[j].y)
						# rad = self.points[i].rad
						# drawPointSizedObject(Window().getWindowReference(), Color.RED.value, coord1, rad)
						# drawPointSizedObject(Window().getWindowReference(), Color.RED.value, coord2, rad)
						self.collisions += 1
					j += 1
				i += 1
			return self.collisions
	
		# recurse on children
		for i in range(4):
			self.collisions += self.children[i].count_collisions()
		return self.collisions

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