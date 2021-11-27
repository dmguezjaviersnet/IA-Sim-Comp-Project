import sys , pygame
from buildgraph import buildgraph
from Graph import  Graph

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ROCKCOLOR = (100,50,0)

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

src = (2,0) 
dest = (7,8)
rocks = [(1,2), (2,2), (3,0), (3,1), (2,1),
         (3,4), (2,4), (2,5), (2,6), (1,6),
         (1,8), (2,8), (3,8), (3,9),
         (5,1), (5,2), (5,3), (6,2),
         (7,0), (8,0),
         (8,2), (8,3), (8,4), (9,4),
         (5,6), (5,8), (5,9), (6,5), (6,6), (6,7), (6,8), (7,7), (8,6), (8,7), (8,8)]

def drawGrid(rows,columns, walk):
  blockSize = WINDOW_WIDTH // rows 
  
  for x in range (rows):
    for y in range (columns):
      rect = pygame.Rect(y*blockSize + 1,x*blockSize + 1 ,blockSize -2 ,blockSize-2)
      rect1 = pygame.Rect(y*blockSize ,x*blockSize  ,blockSize ,blockSize)
      if (x,y) == src:
        pygame.draw.rect(SCREEN,BLUE,rect,width=0, border_radius=1)
        pygame.draw.rect(SCREEN,BLACK,rect1,width=1, border_radius=2)
      elif (x,y) == dest:
        pygame.draw.rect(SCREEN,RED,rect,width=0, border_radius=1)
        pygame.draw.rect(SCREEN,BLACK,rect1,width=1, border_radius=2)
      elif (x,y) in rocks:
        pygame.draw.rect(SCREEN,ROCKCOLOR,rect)
        pygame.draw.rect(SCREEN,BLACK,rect1, width=1)
      elif (x,y) in walk:
        pygame.draw.rect(SCREEN,YELLOW,rect,width=0, border_radius=1)
        pygame.draw.rect(SCREEN,BLACK,rect1,width=1, border_radius=2)
      else:
        pygame.draw.rect(SCREEN,BLACK,rect,2)



if __name__ == '__main__':
  global SCREEN, CLOCK
  pygame.init()
  SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
  CLOCK = pygame.time.Clock()
  SCREEN.fill(WHITE)

  count = 0 
  rows = 10 
  columns = 10 

  G = buildgraph(rows,columns,rocks)
  graph = Graph([],G,rows,columns)
  track = graph.astar(21,79)
  walk = []
  index = 0 
  while(True):
    if count < 1000000:
      count = count + 1 
    if ((count % 300) == 0) and index < len(track):
      position = track[index]-1
      x,y = position // columns , position % columns
      walk.append((x,y))
      index = index + 1

    drawGrid(rows,columns, walk)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit() 
    pygame.display.update()


