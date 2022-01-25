from abc import abstractmethod
from Automaton import Automaton

class Node:

    '''Objeto para representar nodos de AST para REGEX'''

    @abstractmethod
    def eval(self):
        ...

class AtomicNode(Node):

    def __init__(self, value):
        self.value = value

class UnaryNode(Node):
    def __init__(self, node: 'Node'):
        self.node = node
    
    def eval(self):
        value = self.node.eval()
        return self.operate(value)
    
    
    @abstractmethod
    def operate(self, value):
        ...

class BinaryNode(Node):
    def __init__(self, left: 'Node', right: 'Node'):
        self.left  = left
        self.right = right
    
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        return self.operate(left, right)
    
    
    @abstractmethod
    def operate(self, lvalue, rvalue):
        raise NotImplementedError


class EpsilonNode(AtomicNode):
    def eval(self):
        return Automaton(number_of_states=1, initial_state=0, finalStates=[0], transitions={})


class SymbolNode(AtomicNode):
    def eval(self):
        symbol = self.value
        return Automaton(number_of_states=2, initial_state=0, finalStates=[1], transitions={(0,symbol):[1]})

class ClosureNode(UnaryNode):
        
    def operate(self, value: 'Automaton')-> 'Automaton':
        return Automaton.automaton_closure(value)

class UnionNode(BinaryNode):

    def operate(self, lvalue: 'Automaton', rvalue: 'Automaton') -> 'Automaton':
        return Automaton.automaton_union(lvalue, rvalue)

class ConcatNode(BinaryNode):

    def operate(self, lvalue: 'Automaton', rvalue: 'Automaton') -> 'Automaton':
        return lvalue + rvalue

class RangeNode(BinaryNode):

    def eval(self):
        left = self.left.value
        right = self.right.value
        return self.operate(left, right)

    def operate(self, lvalue, rvalue):
        return Automaton(number_of_states=2, initial_state=0, finalStates=[1], 
        transitions={(0,chr(ascii_v)): [1] for ascii_v in range(ord(lvalue), ord(rvalue)+1)})



    