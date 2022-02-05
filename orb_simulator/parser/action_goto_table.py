from typing import List
from parser.non_terminal import Non_terminal
from parser.terminal import Terminal

class Action_Goto_Table:
    """Tabla Action-Goto, separados los terminales de los no terminales"""
    def __init__(self, terminals: List[Terminal], non_terminals: List[Non_terminal]):
        self.terminals_dict = {terminal.identifier: {} for terminal in terminals}
        self.non_terminals_dict = {nt.identifier: {} for nt in non_terminals}