from orbsim_language.orbsim_ast.atomic_node import AtomicNode

class StringNode(AtomicNode):
    def __init__(self, val: str):
        super.__init__(val)
        self.type = 'String'