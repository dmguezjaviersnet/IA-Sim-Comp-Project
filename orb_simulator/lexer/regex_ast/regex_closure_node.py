from lexer.regex_ast.regex_unary_node import UnaryNode
from automaton.automaton import Automaton

class ClosureNode(UnaryNode):
        
    def operate(self, value: 'Automaton')-> 'Automaton':
        return Automaton.automaton_closure(value)