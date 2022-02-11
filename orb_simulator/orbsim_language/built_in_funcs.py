from orbsim_language.orbsim_ast.string_node import StringNode
from orbsim_language.instance import Instance

def concat(s1: StringNode, s2: StringNode):
    return Instance( s1 + s2)