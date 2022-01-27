from ExpressionNode import ExpressionNode
from dataclasses import dataclass

@dataclass
class ConditionalExprNode(ExpressionNode):
    if_expr: ExpressionNode
    then_expr: ExpressionNode
    else_expr: ExpressionNode