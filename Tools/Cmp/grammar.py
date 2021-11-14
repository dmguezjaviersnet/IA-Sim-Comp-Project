from non_terminal import *
from terminal import *
from production import *


class Grammar:

    def __init__(self, terminals, non_terminals: list[Terminal], initial_nt: list[Non_terminal], productions: list[Production]):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.initial_nt = initial_nt
        self.productions = productions

