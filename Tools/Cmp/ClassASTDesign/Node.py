from enum import Enum
from typing import List


class Symbol(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3
    LEFT = 4
    RIGHT = 5
    E = 6
    T = 7

class Node:
    
    symbol: Symbol
    children: List['Node']
    

    def __init__(self):
        pass