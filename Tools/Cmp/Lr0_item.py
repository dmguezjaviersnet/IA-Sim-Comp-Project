from typing import Tuple
from Non_terminal import Non_terminal
from Own_symbol import Symbol

class Lr0_item:
    
    """docstring for Lr0_item."""

    def __init__(self, head: Non_terminal, tail: Tuple[Symbol], dot: int):
        self.head: Non_terminal = head;
        self.tail: Tuple[Symbol] = tail;
        self.dot: int = dot;

    def __str__(self) -> str:
        lr0_id = f'{self.head.identifier} -> ' # id de la cabeza de la producción

        for elem in self.tail:
            lr0_id += f'{elem.identifier} '
        
        return lr0_id

    @property
    def __key(self):
        return (self.head, self.tail, self.dot)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Lr0_item):
            if self.head.identifier != __o.head.identifier or len(self.tail) != len(__o.tail) or self.dot != __o.dot:
                return False
            
            for elem1, elem2 in zip(self.tail, __o.tail):
                if elem1.identifier != elem2.identifier:
                    return False

            return True

        return False

    def __hash__(self) -> int:
        return hash(self.__key)