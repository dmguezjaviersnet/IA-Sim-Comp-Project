from typing import List
from Non_terminal import *
from Terminal import *
from Production import *


class Grammar:

    def __init__(self, terminals, non_terminals: List[Terminal], initial_nt: List[Non_terminal], productions: List[Production]):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.initial_nt = initial_nt
        self.productions = productions

        self.map_prodstr_rules: dict[str, tuple[Callable, bool]] = self.__map_rules()

    def __map_rules(self):
        ans: dict[str, tuple[Callable, bool]] = {}
        
        for i in range(len(self.productions)):
            head_id = self.productions[i].head.identifier + ' -> '
            for j in range(len(self.productions[i].tails)):
                tail_id = ''
                for elem in self.productions[i].tails[j]:
                    tail_id += elem.identifier + ' '
                ans[head_id + tail_id] = self.productions[i].rules[j]
        return ans