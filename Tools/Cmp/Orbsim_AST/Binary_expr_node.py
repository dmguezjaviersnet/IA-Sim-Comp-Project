from dataclasses import dataclass
from Tools.Cmp.Orbsim_AST.expression_node import Expression_node

@dataclass
class Binary_expr_node(Expression_node):
    left: 'Expression_node'
    right:'Expression_node'
    operator: str