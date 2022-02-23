# class Tag(Enum):
#     NONE = 0
#     SELECTED = 1
#     NEIGHBOR = 2



# @dataclass
# class QuadNodeData:
#     container_rect : Tuple[Point, Point]
#     index: int
#     depth: int

#     def __hash__(self) -> int:
#         return hash((self.container_rect, self.index, self.depth))

# @dataclass
# class QuadElement:
#     object: Any
#     x_start: int
#     x_end: int
#     y_start: int
#     y_end: int

# @dataclass
# class QuadEltNode:
#     next_element: int
#     element: int
    
# @dataclass
# class QuadTreeNode: 
#     first_child: int
#     count: int

# class QuadTree:

#     def __init__(self, elements: List[OrbsimObj], boundaries: Tuple[Point, Point], max_depth: int, world_size: int) -> None:
#         self.elements: QuadElement = [QuadElement(elem, elem.upper_left_pos.x, elem.lower_righ_pos.x, elem.upper_left_pos.y, elem.lower_righ_pos.y) for elem in elements]
#         self.boundaries = boundaries
#         self.free_node = 1
#         self.nodes = [QuadTreeNode(-1, 0)]
#         self.elements_nodes: List[QuadEltNode] = []
#         self.max_depth = max_depth
#         self.world_size = world_size
        
    # def insert(self, object: SpaceDebris):
    #     upper_bound = Point(self.origin.x + self.size, self.origin.y + self.size)

    #     if object.position < self.origin or object.position > upper_bound:
    #         return

    #     if self.depth < MAX_DEPTH:
    #         cuadrant = self.__get_cuadrant(object.position)

    #         if not self.children:
    #             self.children = [None for i in range(4)]
    #             if cuadrant == Child.NW:
    #                 self.children[cuadrant] = QuadTree(self.size / 2, self.depth + 1, Point(self.origin.x, self.origin.y))

    #             elif cuadrant == Child.NE:
    #                 self.children[cuadrant] = QuadTree(self.size / 2, self.depth + 1, Point((self.origin.x + self.size) / 2, self.origin.y))

    #             elif cuadrant == Child.SW:
    #                 self.children[cuadrant] = QuadTree(self.size / 2, self.depth + 1, Point(self.origin.x, (self.origin.y + self.size)/ 2))

    #             else:
    #                 self.children[cuadrant] = QuadTree(self.size / 2, self.depth + 1, Point((self.origin.x + self.size) / 2, (self.origin.y + self.size)/ 2))
    #             self.children[cuadrant].insert(object)

    #         else: 
    #             self.children[cuadrant].insert(object)

    # def find(self, object: SpaceDebris) -> bool:
    #     upper_bound = Point(self.origin.x + self.size, self.origin.y + self.size)
        
    #     if object.position < self.origin or object.position > upper_bound:
    #       return False

    #     if self.depth < MAX_DEPTH:
    #         cuadrant = self.__get_cuadrant(object.position)

    #         if not self.children[cuadrant]:
    #             if any(elem == object for elem in self.objects):
    #                 return True

    #             return False

    #         else:
    #             return self.children[cuadrant].find(object)

    #     return False

    # def __get_cuadrant(self, position: Point) -> int:
    #     pos = -1
    #     midx = (self.origin.x + self.size) / 2
    #     midy = (self.origin.y + self.size) / 2

    #     if position.x <= midx:
    #             if position.y <= midy:
    #                 pos = Child.NW
    #             else:
    #                 pos = Child.SW

    #     else:
    #         if position.y <= self.origin.y:
    #             pos = Child.NE
    #         else:
    #             pos = Child.SE

    #     return pos
          
   

    # def build_grid(self):
    #     leaves = set()
    #     root_data = QuadNodeData((self.boundaries), 0, 0)
    #     for index, elem in enumerate(self.elements):
    #         leaves = leaves.union(self.find_leaves(root_data, (elem.x_start, elem.y_start, elem.x_end, elem.y_end), index))

    # def split_node(self, node_index):
    #     for i in range(1, 5):
    #         self.nodes.insert(node_index*4 + i, QuadTreeNode(-1, 0))
    
    # # def update_

    # def insert(self, element: OrbsimObj):
    #     x_start = element.upper_left_pos.x
    #     y_start = element.upper_left_pos.y
    #     x_end = element.lower_righ_pos.x
    #     y_end = element.lower_righ_pos.y
    #     self.elements.append(QuadElement(element, x_start, x_end, y_start, y_end))

    # def update_leaves(self, root: QuadNodeData, first_elem: int):
    #     updated_leaves = set()
    #     dummy_elem_index = first_elem
    #     while dummy_elem_index != -1:
    #         curr_elem = self.elements[self.elements_nodes[dummy_elem_index].element]
    #         elem_container = (curr_elem.x_start, curr_elem.y_start, curr_elem.x_end, curr_elem.y_end)

    #         updated_leaves = updated_leaves.union(self.find_leaves(root, elem_container, self.elements_nodes[dummy_elem_index].element))

    #         prev_dummy = dummy_elem_index
    #         dummy_elem_index = (self.elements_nodes[dummy_elem_index].next_element - 1 if self.elements_nodes[dummy_elem_index].next_element > dummy_elem_index
    #                             else self.elements_nodes[dummy_elem_index].next_element)

    #         del self.elements_nodes[prev_dummy]
            
    #         for _, elem in enumerate(self.elements_nodes):
    #             if elem.next_element > prev_dummy:
    #                 elem.next_element -= 1
            
    #         for _, elem in enumerate(self.nodes):
    #             if elem.count > 0:
    #                 if elem.first_child > prev_dummy:
    #                     elem.first_child -= 1
                    

    #     return updated_leaves

    # def find_leaves(self, root: QuadNodeData, obj_rect: Tuple[int, int, int, int], elt_index: int):
    #     leaves = set()
    #     nodes_remaining = [root]
        
    #     while(nodes_remaining):
    #         node_data = nodes_remaining.pop()
    #         if node_data.depth < self.max_depth:
    #             if self.nodes[node_data.index].count != -1:
    #                 if self.nodes[node_data.index].count + 1 >= 3:

    #                     low_x = node_data.container_rect[0].x
    #                     low_y = node_data.container_rect[0].y
    #                     mid_x = node_data.container_rect[1].x >> 1
    #                     mid_y = node_data.container_rect[1].y >> 1
    #                     first_child = self.nodes[node_data.index].first_child

    #                     right = low_x + mid_x
    #                     down = low_y + mid_y

    #                     nodes_created = 0
    #                     if obj_rect[1] <= mid_y:
    #                        if obj_rect[0] <= mid_x:
    #                             nodes_remaining.append(QuadNodeData((Point(low_x, low_y), Point(mid_x, mid_y)), 4*first_child + 1, node_data.depth+1));
    #                             nodes_created += 1

    #                        if obj_rect[2] > mid_x:
    #                             nodes_remaining.append(QuadNodeData((Point(right, low_y), Point(down, node_data.container_rect[2])), 4*first_child + 2, node_data.depth + 1));
    #                             nodes_created += 1


    #                     if obj_rect[3] > mid_y:
    #                        if obj_rect[0] <= mid_x:
    #                             nodes_remaining.append(QuadNodeData((Point(down, low_y), Point(right, node_data.container_rect[3])), 4*first_child + 3, node_data.depth + 1));
    #                             nodes_created += 1

    #                        if obj_rect[2] > mid_x:
    #                             nodes_remaining.append(
    #                                QuadNodeData((Point(mid_x, mid_y), Point(node_data.container_rect[2], node_data.container_rect[3])), 4*first_child + 4, node_data.depth + 1));
    #                             nodes_created += 1

    #                     self.split_node(node_data.index)
    #                     self.nodes[node_data.index].count = -1

    #                     for index in range(nodes_created):
    #                         new_node_data = nodes_remaining[len(nodes_remaining) - nodes_created + index]
    #                         first_child = self.nodes[node_data.index].first_child
    #                         self.update_leaves(new_node_data, first_child)

    #                     self.nodes[node_data.index].first_child = 4*node_data.index + 1

    #                 else:
    #                     leaves.add(node_data)
    #                     self.nodes[node_data.index].count += 1

    #                     first_elt_node_index = self.nodes[node_data.index].first_child

    #                     if first_elt_node_index != -1:
    #                         while self.elements_nodes[first_elt_node_index].next_element != -1:
    #                             first_elt_node_index = self.elements_nodes[first_elt_node_index].next_element

    #                         self.elements_nodes.append(QuadEltNode(-1, elt_index))
    #                         self.elements_nodes[first_elt_node_index].next_element = len(self.elements_nodes) - 1
                        
    #                     else: 
    #                         self.elements_nodes.append(QuadEltNode(-1, elt_index))
    #                         self.nodes[node_data.index].first_child = len(self.elements_nodes) - 1

    #             else:
    #                 leaves.add(node_data)
    #                 self.nodes[node_data.index].count += 1
                    
    #         else:
    #             leaves.add(node_data)
    #             self.nodes[node_data.index].count += 1

    #             elt_node = self.elements_nodes[self.nodes[node_data.index].first_child]
    #             while elt_node.next_element != -1:
    #                 elt_node = self.element_nodes[elt_node]
                
    #             new_elt_node = QuadEltNode(-1, elt_index)
    #             self.elements_nodes.append(new_elt_node)
    #             elt_node.next_element = len(self.elements_nodes) - 1

    #     return leaves