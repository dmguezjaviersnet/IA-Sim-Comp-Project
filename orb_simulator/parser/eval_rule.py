from typing import Callable, List
from parser.non_terminal import Non_terminal
from parser.own_symbol import Symbol

def eval_rule(rule: Callable, head: Non_terminal, tail: List[Symbol]):
    rule(head, tail)