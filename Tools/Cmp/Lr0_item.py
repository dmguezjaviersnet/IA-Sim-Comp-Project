from typing import List
from Non_terminal import Non_terminal
from Own_symbol import Symbol


class Lr0_item:
    
    """docstring for Lr0_item."""

    def __init__(self, head: Non_terminal, tail: List[Symbol], dot: int):
        self.head: Non_terminal = head;
        self.tail: List[Symbol] = tail;
        self.dot: int = dot;
                
        