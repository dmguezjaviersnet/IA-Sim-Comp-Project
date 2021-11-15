from typing import Callable
from non_terminal import *
from own_symbol import Symbol

class Production:
    def __init__(self, head: Non_terminal, tails: list[list[Symbol]], rules: list[list[tuple[Callable, bool]]]):
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

