from lexer.regex_ast.regex_atomic_node import AtomicNode
from automaton import Automaton

class EpsilonNode(AtomicNode):
    def eval(self):
        return Automaton(number_of_states=1, initial_state=0, finalStates=[0], transitions={})