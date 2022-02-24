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