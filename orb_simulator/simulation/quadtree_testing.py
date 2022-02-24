# from typing import List, Tuple
# import pygame
# import random
# from enum import Enum, IntEnum
# from orbsim_simulation_entities import OrbsimObj, Point, SpaceDebris, OrbsimAgent

# # Function to check if a 'point' is contained in a 'region'
# def contained(object: OrbsimObj, region: Tuple[int, int]):
# 	top_left = region[0]
# 	top_left_x = top_left.x
# 	top_left_y = top_left.y
# 	bottom_right = region[1]
# 	bottom_right_x = bottom_right.x
# 	bottom_right_y = bottom_right.y

# 	obj_top_left_x = object.top_left.x
# 	obj_top_left_y = object.top_left.y
# 	obj_bottom_right_x = object.bottom_right.x
# 	obj_bottom_right_y = object.bottom_right.y

# 	checkX = (obj_top_left_x >= top_left_x) or (obj_bottom_right_x <= bottom_right_x)
# 	checkY = (obj_top_left_y >= top_left_y) or (obj_bottom_right_y <= bottom_right_y)
# 	return checkX and checkY

# # Function to check if two circles are colliding
# def detectCircleCollision(point1, point2):
# 	# point1, point2 are the circles
# 	dx = point2.x - point1.x
# 	dy = point2.y - point1.y
# 	combinedRadii = point1.rad + point2.rad

# 	# Distance formula
# 	if ((dx * dx) + (dy * dy) < combinedRadii * combinedRadii):
# 		return True
# 	return False



# def drawPointSizedObject(windowScreen, color, coords, rad,width = 0):
# 	pygame.draw.circle(windowScreen,color,coords,rad,width)

# def drawBoxSizedObject(windowScreen, color, coords: Tuple[Point, Point], width=0):
# 	pygame.draw.rect(windowScreen, color, (coords[0].x, coords[0].y, coords[1].x-coords[0].x, coords[1].y-coords[0].y))

# def setWindowCaption(caption):
# 	pygame.display.set_caption(caption)

# # Quad Tree Node data structure	


# def main():
# 	window = Window()
# 	windowRef = window.getWindowReference()
# 	objects_amount = 50
# 	collectors_amount = 1;
# 	setWindowCaption("Collision Detection Using Quad Trees")

# 	objects: List[OrbsimObj] = []
# 	collectors: List[OrbsimAgent]
# 	for i in range(objects_amount):
# 		top_left_x = int(round(random.uniform(0, window.getWidth())))
# 		top_left_y = int(round(random.uniform(0, window.getHeight())))
# 		# bottom_right_x = int(round(random.uniform(0, window.getWidth())))
# 		# bottom_right_y = int(round(random.uniform(0, window.getHeight())))
# 		width = int(round(random.uniform(30, 45)))
# 		height = int(round(random.uniform(20, 25)))
# 		bottom_right_x = top_left_x + width
# 		bottom_right_y = top_left_y + height

# 		speed = Point(round(random.uniform(0, 5)), round(random.uniform(0, 5)))
		
# 		# if top_left_x > bottom_right_x:
# 		# 	temp = top_left_x
# 		# 	top_left_x = bottom_right_x
# 		# 	bottom_right_x = temp
		
# 		# if top_left_y > bottom_right_y:
# 		# 	temp = top_left_y
# 		# 	top_left_y = bottom_right_y
# 		# 	bottom_right_y = temp


# 		# if i == 0:
# 		# 	object = SpaceDebris((Point(375, 75), Point(382, 77)), 3, f'sd{i}')
			
# 		# if i == 1:
# 		# 	object = SpaceDebris((Point(1006, 163), Point(1017, 167)), 3, f'sd{i}')

# 		# if i == 2:   
# 		# 	object = SpaceDebris((Point(79, 909), Point(91, 918)), 3, f'sd{i}')
		
# 		# if i == 3:	
# 		# 	object = SpaceDebris((Point(375, 1007), Point(378, 1015)), 3, f'sd{i}')

# 		# if i == 4:
# 		# 	object = SpaceDebris((Point(923, 764), Point(930, 772)), 3, f'sd{i}')

# 		# if i == 5:
# 		# 	object = SpaceDebris((Point(664, 822), Point(677, 831)), 3, f'sd{i}')
		
# 		# if i == 6:
# 		# 	object = SpaceDebris((Point(100, 150), Point(150, 300)), 3, f'sd{i}')
                                                                                                                               
# 		object = SpaceDebris((Point(top_left_x, top_left_y), Point(bottom_right_x, bottom_right_y)), 3, speed, f'sd{i}')
# 		objects.append(object)

# 		for i in range(collectors_amount):
# 			pass

# 	done = False
# 	clock = pygame.time.Clock()
# 	windowRef.fill(Color.WHITE.value)
# 	while not done:
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				done = True

# 		# draw here
# 		windowRef.fill(Color.WHITE.value)
		
# 			if object.bottom_right.x == window.getWidth() or object.top_left.x == 0:
# 				object.orientation_x = -1 * object.orientation_x

# 			if object.bottom_right.y == window.getHeight() or object.top_left.y == 0:
# 				object.orientation_y = -1 * object.orientation_y

# 			object.top_left.set_x(max(min(object.top_left.x + object.speed.x*object.orientation_x, window.getWidth()),0))
# 			object.top_left.set_y(max(min(object.top_left.y + object.speed.y*object.orientation_y, window.getHeight()),0))
# 			object.bottom_right.set_x(max(min(object.bottom_right.x + object.speed.x*object.orientation_x, window.getWidth()),0))
# 			object.bottom_right.set_y(max(min(object.bottom_right.y + object.speed.y*object.orientation_y, window.getHeight()),0))

# 			drawBoxSizedObject(windowRef, Color.BLACK.value, [object.top_left, object.bottom_right], 2)
			
		
		

# 		# qTree.find_collisions()
# 		pygame.display.flip()

# 		# print(qTree.collisions)
# 		print(len(leaves))
# 		# for object in objects:
# 		# 	print(object.top_left.x, object.top_left.y, object.bottom_right.x, object.bottom_right.y)
# 		# free any unreferenced memory to avoid defragmentation. Possible perfomance improvements.
# 		clock.tick(int(60)) # fps

# 	pygame.quit()

# if __name__ == '__main__':
# 	pygame.init()
# 	main()

import pygame
import math
import sys
import random
import gc
from enum import Enum

class Point:
	def __init__(self,x,y, fx = 1, fy = 1, radius = 3):
		self.x = x
		self.y = y
		self.fx = fx
		self.fy = fy
		self.rad = radius

	def addPoint(self,p):
		return Point(self.x + p.x, self.y + p.y)

	def setX(self,x):
		self.x = x

	def setY(self,y):
		self.y = y

	def updateVelocity(self,velocity):
		self.velocity = velocity	

class Window:
	width = 800
	height = 500
	windowScreen = pygame.display.set_mode([width,height])

	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width

	def getWindowReference(self):
		return self.windowScreen


class Color(Enum):
	WHITE = (255,255,255)
	GREEN = (0,255,0)
	BLACK = (0,0,0)
	RED = (255,0,0)
	BLUE = (0,0,255)

# Function to check if a 'point' is contained in a 'region'
def contained(point, region):
	topLeft = region[0]
	lowerX = topLeft.x
	lowerY = topLeft.y
	bottomRight = region[1]
	higherX = bottomRight.x
	higherY = bottomRight.y

	checkX = (point.x >= lowerX) and (point.x <= higherX)
	checkY = (point.y >= lowerY) and (point.y <= higherY)
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

def drawLine(windowScreen, color, point1, point2):
	pygame.draw.line(windowScreen, color, point1,point2)

def drawPointSizedObject(windowScreen, color, coords, rad,width = 0):
	pygame.draw.circle(windowScreen,color,coords,rad,width)


def setWindowCaption(caption):
	pygame.display.set_caption(caption)

# Quad Tree Node data structure	
class QTNode:
	def __init__(self):
		self.children = []
	
	# returns true if a node is a leaf in the quadtree
	def isLeaf(self):
		for child in self.children:
			if child is not None:
				return False
		return True

# Quad Tree data structure
class QuadTree:
	def __init__(self, boundingBox):
		self.root = None
		self.boundingBox = boundingBox # bounding box is a property of the QTree and not the QTNode
		self.points = []
		self.maxLimit = 
		self.collisions = 0
	
	# returns true if quadtree is empty
	def isEmpty(self):
		return self.root == None

	# returns first reference to where the point should be inserted
	def find(self,qtree,point):
		if (qtree.root.isLeaf()): # invariant: if its a leaf, it has to be present in bounding box
			return self
		for i in range(4):
			q = qtree.root.children[i]
			if (contained(point, q.boundingBox)):
				if (q.isEmpty()):
					return q
				return q.find(q,point)

		return self # should never get here .. 
	
	# inserts a point into the quadtree
	def insert(self,point):
		if (not contained(point, self.boundingBox)):
			return

		if (self.isEmpty()):
			self.root = QTNode()
			self.points.append(point)
			return

		q = self.find(self, point)
		if (q.isEmpty()):
			q.root = QTNode()
			q.points.append(point)

		elif (q.root.isLeaf() and len(q.points) < q.maxLimit):
			q.points.append(point)

		elif (q.root.isLeaf()):
			q.points.append(point)
			q.split()

		else: # not a leaf
			for child in q.root.children:
				child.insert(point)


	# splits current quad tree into 4 smaller quad trees
	def split(self):
		if (self.isEmpty()):
			return
		topLeft = self.boundingBox[0]
		lowerX = topLeft.x
		lowerY = topLeft.y
		bottomRight = self.boundingBox[1]
		higherX = bottomRight.x
		higherY = bottomRight.y

		meanX = (lowerX + higherX)/2
		meanY = (lowerY + higherY)/2
		q1 = QuadTree((Point(meanX, lowerY), Point(higherX, meanY)))
		q2 = QuadTree((Point(lowerX,lowerY), Point(meanX, meanY)))
		q3 = QuadTree((Point(lowerX, meanY), Point(meanX, higherY)))
		q4 = QuadTree((Point(meanX, meanY), Point(higherX, higherY)))

		drawLine(Window().getWindowReference(), Color.BLACK.value, (meanX, lowerY), (meanX, higherY))
		drawLine(Window().getWindowReference(), Color.BLACK.value, (lowerX, meanY), (higherX, meanY))

		assert len(self.points) > self.maxLimit
		for point in self.points:
			if (contained(point, q1.boundingBox)):
				q1.insert(point)
			elif (contained(point, q2.boundingBox)):
				q2.insert(point)
			elif (contained(point, q3.boundingBox)):
				q3.insert(point)
			elif (contained(point, q4.boundingBox)):
				q4.insert(point)

		self.root.children = [q1,q2,q3,q4]
	
	# Method to detect collisions for the quadtree built for the frame
	def countCollisions(self):
		# dfs
		if (self.isEmpty()):
			return self.collisions
		if (self.root.isLeaf()):
			# a leaf can contain maximum maxLimit # of objects. So, an n^2 approach here is ok
			i = 0
			numPoints = len(self.points)
			while (i < numPoints):
				j = i + 1
				while (j < numPoints):
					if (detectCircleCollision(self.points[i], self.points[j])):
						coord1 = (self.points[i].x, self.points[i].y)
						coord2 = (self.points[j].x, self.points[j].y)
						rad = self.points[i].rad
						drawPointSizedObject(Window().getWindowReference(), Color.RED.value, coord1, rad)
						drawPointSizedObject(Window().getWindowReference(), Color.RED.value, coord2, rad)
						self.collisions += 1
					j += 1
				i += 1
			return self.collisions
	
		# recurse on children
		for i in range(4):
			self.collisions += self.root.children[i].countCollisions()
		return self.collisions

def main():
	window = Window()
	windowRef = window.getWindowReference()
	limit = int(100)
	setWindowCaption("Collision Detection Using Quad Trees")

	objects = []

	for i in range(limit):
		x = int(round(random.uniform(0,window.width - 1)))
		y = int(round(random.uniform(0, window.height - 1)))
		point = Point(x,y,1,1,4)
		vx = int(round(random.uniform(1,3)));
		vy = int(round(random.uniform(1,3)));
		velocity = Point(vx,vy)
		point.updateVelocity(velocity)
		objects.append(point)

	done = False
	clock = pygame.time.Clock()
	windowRef.fill(Color.WHITE.value)
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		# draw here
		windowRef.fill(Color.WHITE.value)
		qTree = QuadTree((Point(0,0), Point(window.width, window.height)))
		for point in objects:
			if point.x == window.getWidth() or point.x == 0:
				point.fx = -1 * point.fx

			if point.y == window.getHeight() or point.y == 0:
				point.fy = -1 * point.fy

			point.setX(max(min(point.x + point.velocity.x*point.fx, window.getWidth()),0))
			point.setY(max(min(point.y + point.velocity.y*point.fy, window.getHeight()),0))

			drawPointSizedObject(windowRef,Color.BLACK.value,[point.x,point.y],3,0)
			qTree.insert(point)

		qTree.countCollisions()
		pygame.display.flip()

		print(qTree.collisions)
		# free any unreferenced memory to avoid defragmentation. Possible perfomance improvements.
		# gc.collect()
		clock.tick(int(60)) # fps

	pygame.quit()

if __name__ == '__main__':
	pygame.init()
	main()