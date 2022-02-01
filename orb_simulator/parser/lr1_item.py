from typing import FrozenSet, Set
from parser.lr0_item import Lr0_item

class Lr1_item:

    """Item LR(1) para parsing"""

    def __init__(self, center: Lr0_item, look_ahead: FrozenSet[str]):
        self.center = center
        self.look_ahead: Set[str] = look_ahead;

    def __str__(self) -> str:
        ans = f'{self.head.identifier} -> '
        dot_inserted = False
        for index, elem in enumerate(self.tail):
            if not dot_inserted and index == self.center.dot:
                ans += '.'
                continue

            ans += elem.identifier
        
        if not dot_inserted:
            ans += '.'

        ans += str(self.look_ahead)
        
        return ans
    
    @property
    def __key(self):
        return (self.center, self.look_ahead)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Lr1_item):
            if len(self.look_ahead) != len(__o.look_ahead):
                return False

            for elem1, elem2 in zip(self.look_ahead, __o.look_ahead):
                if elem1 != elem2:
                    return False
            
            return True and self.center == __o.center
            
        return False

    def __hash__(self) -> int:
        return hash(self.__key)