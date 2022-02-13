import pygame
import random 

pygame.init()

WEITH , HEIGHT  = 600 , 600

screen = pygame.display.set_mode((WEITH, HEIGHT), 0,32)

RED = (255,0,0)
GREEN =(0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255) 

class equation:
  def __init__(self,m,n):
    self.m = m 
    self.n = n

  def evaluate(self,x):
    return int(x * self.m + self.n)

class objects: 
  def __init__(self,x ,y ):
    self.x = x 
    self.y = y 
    self.size = random .randint(2,6)
    self.step_move = random.randint(1,10)
    self.equation = equation(random.randint(-100,100),random.randint(0,HEIGHT//2))

  
  def move (self):
    self.x = (self.x + self.step_move) % WEITH
    self.y = self.equation.evaluate(self.x)

objects = [objects(random.randint(0,HEIGHT) ,random.randint(0,WEITH)) for i in range(1000)] 

clock = pygame.time.Clock()

while True :
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT: exit()

  for obj in objects:
    obj.move()

  pygame.time.wait(50)
  screen.fill(BLACK)
  
  for obj in objects:
    pygame.draw.circle(screen, RED, (obj.x, obj.y),obj.size)

  pygame.display.update()