from abc import abstractmethod
from regex_ast.regex_node import Node

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