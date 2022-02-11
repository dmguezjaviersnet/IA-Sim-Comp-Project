from orbsim_language.orbsim_ast.string_node import StringNode
from orbsim_language.instance import Instance
from orbsim_language.orbsim_type import*

def concat(s1: 'Instance', s2: 'Instance'):
    return Instance(IntType(), s1.value + s2.value)