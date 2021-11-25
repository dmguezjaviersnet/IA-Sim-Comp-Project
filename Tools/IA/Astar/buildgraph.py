from collections import defaultdict
from pprint import pprint

# array directional
dirr = [-1,-1,-1,0,1,1,1,0]
dirc = [-1,0,1,1,1,0,-1,-1] 

# esto representa los obstaculos, en que coordenadas 
#estan los obstaculos (fila , columna) 
rocks = [(1,2), (2,2), (3,0), (3,1), (2,1),
         (3,4), (2,4), (2,5), (2,6), (1,6),
         (1,8), (2,8), (3,8), (3,9),
         (5,1), (5,2), (5,3), (6,2),
         (7,0), (8,0),
         (8,2), (8,3), (8,4), (9,4),
         (5,6), (5,8), (5,9), (6,5), (6,6), (6,7), (6,8), (7,7), (8,6), (8,7), (8,8)]

# determian si la nueva direcciones es una direccion correcta en el tablero
def positionOk (nr,nc ,rows ,columns):
  return (nr >=0) and (nr < rows) and (nc >= 0) and (nc < columns)


# construye un grafo que representa un tablero de 
# rows filas y columns columnas y con los obstaculos de 
# los que s epasan en la lista de tuplas rokcs
# al final devuelve el grafo que es una instancia  de defaultdict
def buildgraph (rows,columns,rocks):
  G = defaultdict(set)
  n = rows *columns  #amount of nodes

  for i in range (rows):
    for j in range(columns):
      p = (i)* columns +(j) +1
      if (i,j) in rocks : continue
      for r in range(len(dirr)):
        nr , nc = dirr[r] + i , dirc[r] + j
        ap = (nr)* columns + (nc) +1
        g = 10 + ((r+1)%2) * 4 
        if positionOk(nr,nc , rows , columns) and ((nr,nc) not in rocks):
          G[p].add((ap,g))
  return G 