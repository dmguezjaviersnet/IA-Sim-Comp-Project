import time
from typing import List, Tuple
import pygame
import math
import sys
import random
import gc
from enum import Enum, IntEnum
from simulation.orbsim_simulation_entities import OrbsimObj, Point, SpaceDebris, OrbsimAgent
from simulation.generate_objects import*

MAX_DEPTH = 8
MAX_LIMIT = 3
leaves: List['QTNode'] = []

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

# class Point:
# 	def __init__(self,x ,y, fx = 1, fy = 1, radius = 3):
# 		self.x = x
# 		self.y = y
# 		self.fx = fx
# 		self.fy = fy
# 		self.rad = radius

# 	def addPoint(self,p):
# 		return Point(self.x + p.x, self.y + p.y)

# 	def setX(self,x):
# 		self.x = x

# 	def setY(self,y):
# 		self.y = y

# 	def updateVelocity(self,velocity):
# 		self.velocity = velocity	

class Window:
	width = 1024
	height = 1024
	window_screen = pygame.display.set_mode([width,height])
	background = pygame.image.load('./images/bg.jpg').convert()
	screen_center = (window_screen.get_rect().centerx, window_screen.get_rect().centery)
	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width
	def getBackground(self):
		return self.background
	def getScreenCenter(self):
		return self.screen_center
	def getWindowReference(self):
		return self.window_screen


class Color(Enum):
	WHITE = (255,255,255)
	GREEN = (0,255,0)
	BLACK = (0,0,0)
	RED = (255,0,0)
	BLUE = (0,0,255)

# Function to check if a 'point' is contained in a 'region'
def contained(object: OrbsimObj, region: Tuple[int, int]):
	top_left = region[0]
	top_left_x = top_left.x
	top_left_y = top_left.y
	bottom_right = region[1]
	bottom_right_x = bottom_right.x
	bottom_right_y = bottom_right.y

	obj_top_left_x = object.top_left.x
	obj_top_left_y = object.top_left.y
	obj_bottom_right_x = object.bottom_right.x
	obj_bottom_right_y = object.bottom_right.y

	checkX = (obj_top_left_x >= top_left_x) or (obj_bottom_right_x <= bottom_right_x)
	checkY = (obj_top_left_y >= top_left_y) or (obj_bottom_right_y <= bottom_right_y)
	return checkX and checkY

# Function to check if two circles are colliding
def detectCircleCollision(point1, point2):
	# point1, point2 are the circles
	dx = point2.x - point1.x
	dy = point2.y - point1.y
	combinedRadii = point1.rad + point2.rad

	# Distance formula
	if ((dx * dx) + (dy * dy) < combinedRadii * combinedRadii):
		return True
	return False

def detect_overlap(rect1: Tuple[Point, Point], rect2: Tuple[Point, Point]):
	if (rect1[0].x < rect2[1].x and rect1[0].y < rect2[1].y
		and rect1[1].x > rect2[0].x and rect1[1].y > rect2[0].y):
		return True

	return False

def detect_collision(rect1: Tuple[Point, Point], rect2: Tuple[Point, Point]):
	if (rect1[0].x <= rect2[1].x and rect1[0].y <= rect2[1].y
		and rect1[1].x >= rect2[0].x and rect1[1].y >= rect2[0].y):
		return True

	return False

def detect_full_overlap(rect1: Tuple[Point, Point], rect2: Tuple[Point, Point]):
	if (rect1[0].x <= rect2[0].x and rect1[0].y <= rect2[0].y
		and rect1[1].x >= rect2[1].x and rect1[1].y >= rect2[1].y):
		return True

	return False

def drawLine(window_screen, color, point1, point2):
	pygame.draw.line(window_screen, color, point1,point2)

def drawPointSizedObject(window_screen, color, coords, rad,width = 0):
	pygame.draw.circle(window_screen,color,coords,rad,width)

def drawBoxSizedObject(window_screen, color, coords: Tuple[Point, Point], width=0):
	pygame.draw.rect(window_screen, color, (coords[0].x, coords[0].y, coords[1].x-coords[0].x, coords[1].y-coords[0].y))

def setWindowCaption(caption):
	pygame.display.set_caption(caption)

# Quad Tree Node data structure	
class QTNode:
	def __init__(self, parent: 'QTNode', bounding_box: Tuple[Point, Point], depth):
		self.parent = parent
		self.boundingBox = bounding_box # bounding box is a property of the QTree and not the QTNode
		self.depth = depth
		self.children = []
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

		q1 = QTNode(self, (Point(self.boundingBox[0].x, self.boundingBox[0].y), Point(self.center_x, self.center_y)), self.depth + 1)
		q2 = QTNode(self, (Point(self.center_x, self.boundingBox[0].y), Point(self.boundingBox[1].x, self.center_y)), self.depth + 1)
		q3 = QTNode(self, (Point(self.boundingBox[0].x, self.center_y), Point(self.center_x, self.boundingBox[1].y)), self.depth + 1)
		q4 = QTNode(self, (Point(self.center_x, self.center_y), Point(self.boundingBox[1].x, self.boundingBox[1].y)), self.depth + 1)

		drawLine(Window().getWindowReference(), Color.RED.value, (self.center_x, self.boundingBox[0].y), (self.center_x, self.boundingBox[1].y))
		drawLine(Window().getWindowReference(), Color.RED.value, (self.boundingBox[0].x, self.center_y), (self.boundingBox[1].x, self.center_y))

		# assert len(self.objects) > MAX_LIMIT
		for object in self.objects:
			if (detect_overlap((object.top_left, object.bottom_right), q1.boundingBox)):
				q1.insert(object)
			if (detect_overlap((object.top_left, object.bottom_right), q2.boundingBox)):
				q2.insert(object)
			if (detect_overlap((object.top_left, object.bottom_right), q3.boundingBox)):
				q3.insert(object)
			if (detect_overlap((object.top_left, object.bottom_right), q4.boundingBox)):
				q4.insert(object)

		self.children = [q1 ,q2 ,q3 ,q4]
		self.objects.clear()

	def find(self, object: OrbsimObj) -> List['QTNode']:
		if (self.__is_leaf()): # invariant: if its a leaf, it has to be present in bounding box
			return [self]
		
		overlapping_leaves = []
		for i in range(4):
			q_node = self.children[i]
			if (detect_overlap((object.top_left, object.bottom_right), q_node.boundingBox)):
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
				if not detect_full_overlap((object.top_left, object.bottom_right), q_node.boundingBox):
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
            
	def find_neighbors(self):
		all_neighbors = []
		for direction in Direction:
			neighbor = self.find_ge_size_neighbor(direction)
			all_neighbors += self.find_smaller_size_neighbors(neighbor, direction)

		self.neighbors = all_neighbors

# Quad Tree data structure
class QuadTree:
	def __init__(self, bounding_box: Tuple[int, int]):
		self.root = QTNode(None, bounding_box, 0)
		self.collisions = 0

	def insert(self, obj):
		self.root.insert(obj)

	def find_collisions(self):
		self.root.count_collisions()
	
	# returns true if quadtree is empty
	# returns first reference to where the point should be inserted
	

def main():
	window = Window()
	windowRef = window.getWindowReference()
	windowBG = window.getBackground()
	windowCenter = window.getScreenCenter()
	objects_amount = 50
	collectors_amount = 1;
	setWindowCaption("Collision Detection Using Quad Trees")

	objects: List[OrbsimObj] = []
	orbitas = generate_orbits(windowCenter, 18)
	sprites = []
	sprites_group = pygame.sprite.Group()
	for orb in orbitas:
		objs_orb = generate_object_in_orbit(16, orb)
		for obj in objs_orb:
			sprites.append(obj)
			sprites_group.add(obj)
	
	
	collectors: List[OrbsimAgent]
	for i in range(objects_amount):
		top_left_x = int(round(random.uniform(0, window.getWidth())))
		top_left_y = int(round(random.uniform(0, window.getHeight())))
		# bottom_right_x = int(round(random.uniform(0, window.getWidth())))
		# bottom_right_y = int(round(random.uniform(0, window.getHeight())))
		width = int(round(random.uniform(10, 15)))
		height = int(round(random.uniform(8, 12)))
		bottom_right_x = top_left_x + width
		bottom_right_y = top_left_y + height

		speed = Point(round(random.uniform(0, 5)), round(random.uniform(0, 5)))
		
		# if top_left_x > bottom_right_x:
		# 	temp = top_left_x
		# 	top_left_x = bottom_right_x
		# 	bottom_right_x = temp
		
		# if top_left_y > bottom_right_y:
		# 	temp = top_left_y
		# 	top_left_y = bottom_right_y
		# 	bottom_right_y = temp


		# if i == 0:
		# 	object = SpaceDebris((Point(375, 75), Point(382, 77)), 3, f'sd{i}')
			
		# if i == 1:
		# 	object = SpaceDebris((Point(1006, 163), Point(1017, 167)), 3, f'sd{i}')

		# if i == 2:   
		# 	object = SpaceDebris((Point(79, 909), Point(91, 918)), 3, f'sd{i}')
		
		# if i == 3:	
		# 	object = SpaceDebris((Point(375, 1007), Point(378, 1015)), 3, f'sd{i}')

		# if i == 4:
		# 	object = SpaceDebris((Point(923, 764), Point(930, 772)), 3, f'sd{i}')

		# if i == 5:
		# 	object = SpaceDebris((Point(664, 822), Point(677, 831)), 3, f'sd{i}')
		
		# if i == 6:
		# 	object = SpaceDebris((Point(100, 150), Point(150, 300)), 3, f'sd{i}')
                                                                                                                               
		object = SpaceDebris((Point(top_left_x, top_left_y), Point(bottom_right_x, bottom_right_y)), 3, speed, f'sd{i}')
		objects.append(object)

		for i in range(collectors_amount):
			pass

	done = False
	clock = pygame.time.Clock()
	# windowRef.fill(Color.WHITE.value)
	windowRef.blit(windowBG, (0,0))
	while not done:
		max_time = 0
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		# draw here
		windowRef.blit(windowBG, (0,0))
		# windowRef.fill(Color.WHITE.value)
		start = time.time()
		qTree = QuadTree((Point(0,0), Point(window.width, window.height)))
		# for object in objects:
		# 	if object.bottom_right.x == window.getWidth() or object.top_left.x == 0:
		# 		object.orientation_x = -1 * object.orientation_x

		# 	if object.bottom_right.y == window.getHeight() or object.top_left.y == 0:
		# 		object.orientation_y = -1 * object.orientation_y

		# 	object.top_left.set_x(max(min(object.top_left.x + object.speed.x*object.orientation_x, window.getWidth()),0))
		# 	object.top_left.set_y(max(min(object.top_left.y + object.speed.y*object.orientation_y, window.getHeight()),0))
		# 	object.bottom_right.set_x(max(min(object.bottom_right.x + object.speed.x*object.orientation_x, window.getWidth()),0))
		# 	object.bottom_right.set_y(max(min(object.bottom_right.y + object.speed.y*object.orientation_y, window.getHeight()),0))

		# 	drawBoxSizedObject(windowRef, Color.BLUE.value, [object.top_left, object.bottom_right], 2)
		# 	qTree.insert(object)

		for object in sprites:
			qTree.insert(SpaceDebris((Point(object.rect.topleft[0], object.rect.topleft[1]), Point(object.rect.bottomright[0], object.rect.bottomright[1])),
                              0, 0, ''))
		for orb in orbitas:
			orb.draw_elipse(windowRef, (255,0,0))
			
		sprites_group.draw(windowRef)
		sprites_group.update()

		end = time.time()
		if end - start > max_time: 
			max_time = end - start
		
		print(max_time)
		
		# for leaf in leaves:
		# 	leaf.find_neighbors()

		# qTree.find_collisions()
		pygame.display.flip()

		# print(qTree.collisions)
		# print(len(leaves))
		# for object in objects:
		# 	print(object.top_left.x, object.top_left.y, object.bottom_right.x, object.bottom_right.y)
		# free any unreferenced memory to avoid defragmentation. Possible perfomance improvements.
		# gc.collect()
		leaves.clear()
		clock.tick(int(30)) # fps

	pygame.quit()

if __name__ == '__main__':
	pygame.init()
	main()