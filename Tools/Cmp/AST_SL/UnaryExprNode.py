
from ExpressionNode import ExpressionNode
from dataclasses import dataclass


@dataclass
class UnaryExprNode(ExpressionNode):
    expr: ExpressionNode
