from typing import Callable, List, Tuple
from Non_terminal import *
from Own_symbol import Symbol

class Production:
    def __init__(self, head: Non_terminal, tails: List[List[Symbol]], rules: List[List[Tuple[Callable, bool]]]):
        self.head = head
        self.tails = tails
        
        self.nt_in_prod = [0 for i in range(len(self.tails))]
        self.__map_nt_amount()

        self.rules = rules

    
    def __map_nt_amount(self):
        for i in range(len(self.tails)):
            nt_count = 0
            for elem in self.tails[i]:
                if isinstance(elem, Non_terminal):
                    nt_count += 1
            self.nt_in_prod[i] = nt_count

