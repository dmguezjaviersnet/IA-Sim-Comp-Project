import heapq
from simulation.orbsim_simulation_structs.quadtree import QTNode
import math

class NeighborData:
    def __init__(self, value, neighbor) -> None:
        self.value = value
        self.neighbor = neighbor
    
    def __lt__(self, other: 'NeighborData'):
        return self.value < other.value

def eucl_dist_qtnode(qt1: QTNode, qt2: QTNode):
    return math.dist((qt1.center_x, qt1.center_y), (qt2.center_x, qt2.center_y))
    
def reconstruct_path(node: QTNode, parent: QTNode):
    path = [node]

    while node in parent:
        node = parent[node]
        path.insert(0, node)

    return path

def a_star(start: QTNode, h, goal: QTNode, open=None):
    closed_set = set()
    open_set = set()
    g_value = {}
    f_value = []
    parent = {}

    # inicialización
    f_start = h(start, goal)
    g_value[start] = 0
    open_set.add(start)
    heapq.heappush(f_value, NeighborData(f_start, start))

    while open_set:
        curr_data: NeighborData = heapq.heappop(f_value)
        node =  curr_data.neighbor
        node.find_neighbors()

        if goal == node:
            return reconstruct_path(node, parent)

        closed_set.add(node)
        open_set.remove(node)

        for neighbor in node.neighbors:
            tentative_g_score = g_value[node] + 1
            
            if neighbor in closed_set:
                continue

            if neighbor not in open_set or tentative_g_score < g_value[neighbor]:
                parent[neighbor] = node
                g_value[neighbor] = tentative_g_score
                actual_f_value = tentative_g_score + h(neighbor, goal)

                if neighbor in open_set:
                    
                    for i, (p, x) in f_value:
                        if x == neighbor:
                            f_value[i] = NeighborData(actual_f_value, neighbor)
                            break
                    heapq.heapify(f_value)

                else:
                    open_set.add(neighbor)
                    heapq.heappush(f_value, NeighborData(actual_f_value, neighbor))