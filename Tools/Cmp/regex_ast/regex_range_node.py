from regex_ast.regex_binary_node import BinaryNode
from automaton import Automaton

class RangeNode(BinaryNode):

    def eval(self):
        left = self.left.value
        right = self.right.value
        return self.operate(left, right)

    def operate(self, lvalue, rvalue):
        return Automaton(number_of_states=2, initial_state=0, finalStates=[1], 
        transitions={(0,chr(ascii_v)): [1] for ascii_v in range(ord(lvalue), ord(rvalue)+1)})