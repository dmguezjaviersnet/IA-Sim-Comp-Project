from regex_ast.regex_binary_node import BinaryNode
from automaton import Automaton

class UnionNode(BinaryNode):

    def operate(self, lvalue: 'Automaton', rvalue: 'Automaton') -> 'Automaton':
        return Automaton.automaton_union(lvalue, rvalue)