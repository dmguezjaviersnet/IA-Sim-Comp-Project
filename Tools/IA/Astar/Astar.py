from Graph import * 
from heapq import *
from collections import defaultdict
from buildgraph import buildgraph , rocks
from pprint import pprint
from math import fabs, inf

# solo son datos de ejemplo 
rows , columns = 6 , 6
n = rows * columns +1

# Llamda a un modulo aparte para crear el grafo
G = buildgraph(6,6,rocks)

# variables y estructuras basicas para trabajar en el algoritmo
mask = [False] * n
parent = [-1] * n
visited = [False] * n
g = [inf] * n
h = [0] * n
q = []


# funcion heuristica por la que nos guiamos para hacer la 
# mejor aproximacion para llegar a la solucion de forma mas rapida
def heuristic (src,dest):
  x1, x2 = src // columns , src % columns
  y1, y2 = dest // columns , dest % columns
  return  int(fabs(x1 - y1) + fabs(x2 - y2)) 

# para hacer relax a los nodos del grafo 
def relax(src, neighbour,dest, width ):
  if g[src] + width < g[neighbour]:
    g[neighbour] = g[src] + width
    h[neighbour] = heuristic(neighbour,dest)
    parent[neighbour] = src

# funcion A* que calcula el mejor camino siguiendo la 
#heuristica de la funcion heuristic definidas arriba
def Astar(src,dest):
  visited[src]= True
  g[src] = 0
  h[src] = heuristic(src,dest)
  heappush(q,(0,src))

  while len(q)>0:
    _ ,current = heappop(q)

    if current == dest:
      return

    for adyacent in G[current]:
      neighbour , neighbourwidth = adyacent
      relax(current,neighbour,dest,neighbourwidth)

      if not visited[neighbour]:
        heappush(q,(h[neighbour]+ g[neighbour] , neighbour))
        visited[neighbour] = True

# para imprimir el mejor camino 
def printpath (src , dest) :
  path = [dest]
  while dest != src:
    dest = parent[dest]
    path.append(dest)
  path.reverse()
  return path

if __name__ == '__main__':
  Astar(31,7)
  pprint(printpath(31,7))