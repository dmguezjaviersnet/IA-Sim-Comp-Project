from dataclasses import dataclass
import random
import math
from typing import List
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import heapq
import pandas as pd
from collections import OrderedDict

from sklearn import neighbors

@dataclass
class Obj:
    x: int
    y: int
    z: int
    size: float
    def __str__(self):
        return f'Obj({self.x}, {self.y}, {self.z})'




def euclidean_distance_heuristic(obj1: 'Obj', obj2: 'Obj'):
    return math.sqrt((obj1.x -obj2.x)**2 + (obj1.y -obj2.y)**2 + (obj1.z -obj2.z)**2)

x1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]

y1 = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3]

z1 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]

x2 = [1,1,2,1,2,2,1,1,1,2,2,1,1,2,2,2,1,1,2,1,2,2,1,1,2,3,3,1,1,2,3,3,1,1,1,2,2,3,3,3,1,1,1,2,2,3,3,3,1,1,2,3,3,1,1,2,3,3,2,3,3,2,2,3,2,2,3,3,3,2,2,2,3,3,2,3,3,2,2,3,1,1,2,2,1,1,2,2,1,2,1,1,1,2,2,2,1,1,1,2,2,2,1,1,2,2,1,1,2,2,1,1,2,2,1,2,1,1,2,2,3,3,1,1,2,2,3,3,1,1,3,3,1,1,2,2,3,3,1,1,2,2,3,3,1,1,3,3,2,2,3,3,2,2,3,3,2,3,2,2,2,3,3,3,2,2,2,3,3,3,2,2,3,3,2,2,3,3,2,2,3,3,2,3,1,1,2,1,2,2,1,1,1,2,2,1,1,2,2,2,1,1,2,1,2,2,1,1,2,3,3,1,1,2,3,3,1,1,1,2,2,3,3,3,1,1,1,2,2,3,3,3,1,1,2,3,3,1,1,2,3,3,2,3,3,2,2,3,2,2,3,3,3,2,2,2,3,3,2,3,3,2,2,3]

y2 = [1,2,1,2,1,2,1,2,3,1,3,1,3,1,2,3,2,3,3,2,2,3,1,2,1,1,2,1,2,2,1,2,1,2,3,1,3,1,2,3,1,2,3,1,3,1,2,3,2,3,3,2,3,2,3,2,2,3,1,1,2,1,2,2,1,3,1,2,3,1,2,3,1,3,3,2,3,2,3,2,1,2,1,2,1,2,1,2,2,1,1,2,3,1,2,3,1,2,3,1,2,3,1,3,1,3,2,3,2,3,2,3,2,3,2,3,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,2,3,2,3,2,3,2,3,2,3,2,3,2,3,2,3,1,2,1,2,1,2,1,2,1,2,1,2,3,1,2,3,1,2,3,1,2,3,1,3,1,3,2,3,2,3,2,3,2,3,3,2,1,2,1,2,1,2,1,2,3,1,3,1,3,1,2,3,2,3,3,2,2,3,1,2,1,1,2,1,2,2,1,2,1,2,3,1,3,1,2,3,1,2,3,1,3,1,2,3,2,3,3,2,3,2,3,2,2,3,1,1,2,1,2,2,1,3,1,2,3,1,2,3,1,3,3,2,3,2,3,2]

z2 = [2,2,2,1,1,1,2,2,2,2,2,1,1,1,1,1,2,2,2,1,1,1,2,2,2,2,2,1,1,1,1,1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,2,2,2,1,1,1,2,2,2,2,2,1,1,1,1,1,2,2,2,1,1,1,3,3,3,3,1,1,1,1,2,2,3,3,3,3,3,3,1,1,1,1,1,1,2,2,2,2,3,3,3,3,1,1,1,1,2,2,3,3,3,3,3,3,1,1,1,1,1,1,2,2,2,2,3,3,3,3,3,3,1,1,1,1,1,1,2,2,2,2,3,3,3,3,1,1,1,1,2,2,3,3,3,3,3,3,1,1,1,1,1,1,2,2,2,2,3,3,3,3,1,1,1,1,2,2,2,2,2,3,3,3,2,2,2,2,2,3,3,3,3,3,2,2,2,3,3,3,2,2,2,2,2,3,3,3,3,3,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,2,2,2,2,2,3,3,3,3,3,2,2,2,3,3,3,2,2,2,2,2,3,3,3,3,3,2,2,2,3,3,3]


coord_pairs = pd.DataFrame( OrderedDict((('x1', pd.Series(x1)), ('y1', pd.Series(y1)), ('z1', pd.Series(z1)), ('x2', pd.Series(x2)), ('y2', pd.Series(y2)), ('z2', pd.Series(z2)))))

# coord_pairs = coord_pairs.sort_values(['x1', 'y1', 'z1'], ascending=[True,True])

print(coord_pairs)

fig = plt.figure(figsize=(12,12))

def generate_point():
    
    for i in range(20):
        x = random.randint(1,4)
        y = random.randint(1,4)
        z = random.randint(1,4)
        size = random.randint(20,100) * random.random()
        yield Obj(x,y,z,size)

def reconstruct_path(node, parent):
    path = [node]

    while node in parent:
        node = parent[node]
        path.insert(0, node)

    return path

def get_neighbors(node):
    ...
def a_star(start, h, goal, open):
    closed_set = set()
    open_set = set()
    g_value = {}
    f_value = []
    parent = {}

    # inicialización
    f_start = h(start)
    g_value[start] = 0
    open_set.add(start)
    heapq.heappush(f_value, (f_start, start))

    while open_set:
        _, node = heapq.heappop(f_value)

        if goal == node:
            return reconstruct_path(node, parent)

        closed_set.add(node)
        open_set.remove(node)

        for neighbor in get_neighbors(node):
            tentative_g_score = g_value[node] + 1
            
            if neighbor in closed_set:
                continue

            if neighbor not in open_set or tentative_g_score < g_value[neighbor]:
                parent[neighbor] = node
                g_value[neighbor] = tentative_g_score
                actual_f_value = tentative_g_score + h(neighbor)

                if neighbor in open_set:
                    
                    for i, (p, x) in f_value:
                        if x == neighbor:
                            f_value[i] = (actual_f_value, neighbor)
                            break
                    heapq.heapify(f_value)

                else:
                    open_set.add(neighbor)
                    heapq.heappush(f_value, (actual_f_value, neighbor))


def plot_obj(obj:'Obj', ax):
    ax.scatter(obj.x,obj.y,marker = "o", color = "black", s = obj.size)
def graph():
    ax = fig.add_subplot(111)
    for object in generate_point():
        plot_obj(object, ax)
    plt.show()

graph()
# ax.scatter3D(1,1,1,marker = "o", color = "red", s = 10)

# ax.scatter3D(1,2,1,marker = "o", color = "black", s = 2000)

# ax.scatter3D(1,3,1,marker = "o", color = "black", s = 100)

# ax.scatter3D(2,1,1,marker = "o", color = "black", s = 100)

# ax.scatter3D(2,2,1,marker = "o", color = "black", s = 100)

# ax.scatter3D(2,3,1,marker = "o", color = "black", s = 100)

# ax.scatter3D(3,1,1,marker = "o", color = "black", s = 100)

# ax.scatter3D(3,2,1,marker = "o", color = "black", s = 100)

# ax.scatter3D(3,3,1,marker = "o", color = "black", s = 100)

# ax.scatter3D(1,1,2,marker = "o", color = "black", s = 100)

# ax.scatter3D(1,2,2,marker = "o", color = "black", s = 100)

# ax.scatter3D(1,3,2,marker = "o", color = "black", s = 100)

# ax.scatter3D(2,1,2,marker = "o", color = "black", s = 100)

# ax.scatter3D(2,2,2,marker = "x", color = "black", s = 100)

# ax.scatter3D(2,3,2,marker = "o", color = "black", s = 100)

# ax.scatter3D(3,1,2,marker = "o", color = "black", s = 100)

# ax.scatter3D(3,2,2,marker = "o", color = "black", s = 100)

# ax.scatter3D(3,3,2,marker = "o", color = "black", s = 100)

# ax.scatter3D(1,1,3,marker = "o", color = "black", s = 100)

# ax.scatter3D(1,2,3,marker = "o", color = "black", s = 100)

# ax.scatter3D(1,3,3,marker = "o", color = "black", s = 100)

# ax.scatter3D(2,1,3,marker = "o", color = "black", s = 100)

# ax.scatter3D(2,2,3,marker = "o", color = "black", s = 100)

# ax.scatter3D(2,3,3,marker = "o", color = "black", s = 100)

# ax.scatter3D(3,1,3,marker = "o", color = "black", s = 100)

# ax.scatter3D(3,2,3,marker = "o", color = "black", s = 100)
# ax.scatter3D((1,1,3),(2,2,3), (3,1,3), marker = "*", color = "red", s = 100)
# plt.show()
#ax.scatter3D(3,3,3,marker = "o", color = "black", s = 100)
# poisson_process(1000)