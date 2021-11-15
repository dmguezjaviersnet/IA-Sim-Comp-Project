from non_terminal import *
from terminal import *
from production import *


class Grammar:

    def __init__(self, terminals, non_terminals: list[Terminal], initial_nt: list[Non_terminal], productions: list[Production]):
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

