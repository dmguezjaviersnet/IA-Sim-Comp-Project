from regex_ast.regex_node import Node

class AtomicNode(Node):

    def __init__(self, value):
        self.value = value