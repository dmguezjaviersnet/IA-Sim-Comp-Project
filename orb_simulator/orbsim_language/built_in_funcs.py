from orbsim_language.orbsim_ast.string_node import StringNode

def concat(s1: StringNode, s2: StringNode):
    return StringNode(s1 + s2)