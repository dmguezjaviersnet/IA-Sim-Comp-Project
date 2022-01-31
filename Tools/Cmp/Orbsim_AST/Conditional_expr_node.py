from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
from dataclasses import dataclass

@dataclass
class Conditional_expr_node(Expression_node):
    if_expr: 'Expression_node'
    then_expr: 'Expression_node'
    else_expr: 'Expression_node'
