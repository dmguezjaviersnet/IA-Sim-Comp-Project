from orbsim_ast.expression_node import ExpressionNode
from dataclasses import dataclass


@dataclass
class UnaryExprNode(ExpressionNode):
    expr: 'ExpressionNode'
    operator: str

