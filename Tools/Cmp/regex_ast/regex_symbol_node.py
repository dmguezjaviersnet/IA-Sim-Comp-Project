from regex_ast.regex_atomic_node import AtomicNode
from automaton import Automaton

class SymbolNode(AtomicNode):
    def eval(self):
        symbol = self.value
        return Automaton(number_of_states=2, initial_state=0, finalStates=[1], transitions={(0,symbol):[1]})