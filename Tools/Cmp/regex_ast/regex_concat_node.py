from regex_ast.regex_binary_node import BinaryNode
from automaton import Automaton

class ConcatNode(BinaryNode):

    def operate(self, lvalue: 'Automaton', rvalue: 'Automaton') -> 'Automaton':
        return lvalue + rvalue