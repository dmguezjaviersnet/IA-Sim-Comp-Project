from typing import List
from non_terminal import *
from terminal import *
from production import *


class Grammar:

    def __init__(self, terminals, non_terminals: List[Terminal], initial_nt: List[Non_terminal], productions: List[Production]):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.initial_nt = initial_nt
        self.productions = productions
        self.symbols_dicc = {};
