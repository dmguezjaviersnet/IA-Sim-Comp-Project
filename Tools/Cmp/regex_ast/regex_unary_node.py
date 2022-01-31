from abc import abstractmethod
from regex_ast.regex_node import Node

class UnaryNode(Node):
    def __init__(self, node: 'Node'):
        self.node = node
    
    def eval(self):
        value = self.node.eval()
        return self.operate(value)
    
    
    @abstractmethod
    def operate(self, value):
        ...