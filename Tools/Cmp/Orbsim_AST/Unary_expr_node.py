
from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
from Unary_expr_node import UnaryExprNode
from dataclasses import dataclass


@dataclass
class UnaryExprNode(Expression_node):
    expr: 'Expression_node'
    operator: str

