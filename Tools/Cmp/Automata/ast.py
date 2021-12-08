from abc import abstractmethod
from automaton import *

class Node:
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
    def operate(value):
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
    def operate(lvalue, rvalue):
        ...


class EpsilonNode(AtomicNode):
    def eval(self):
        return NFA(nStates=1, q0 = 0, finalStates=[0], transitions={})


class SymbolNode(AtomicNode):
    def eval(self):
        symbol = self.value
        return DFA(nStates=2, q0 = 0, finalStates=[1], transitions={(0,symbol):1})

class ClosureNode(UnaryNode):
    
    def operate(value):
         return AutomatonClosure(value)

class UnionNode(BinaryNode):

    def operate(lvalue, rvalue):
        return AutomatonUnion(lvalue, rvalue)

class ConcatNode(BinaryNode):

    def operate(lvalue, rvalue):
        return AutomatonConcat(lvalue, rvalue)

        