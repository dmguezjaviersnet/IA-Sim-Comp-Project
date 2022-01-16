from typing import List, Set
from Production import Production
from Lr0_item import Lr0_item
from Non_terminal import Non_terminal
from Own_symbol import Symbol

class Lr1_item:

    """Item LR(1) para parsing"""

    def __init__(self, center: Lr0_item, look_ahead: Set[str]):
        self.center = center
        self.look_ahead: Set[str] = look_ahead;

    def __str__(self) -> str:
        ans = f'{self.head.identifier} -> '
        for elem in self.tail:
            ans += elem.identifier
        
        return ans