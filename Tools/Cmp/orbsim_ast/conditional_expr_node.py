from orbsim_ast.expression_node import ExpressionNode
from dataclasses import dataclass

@dataclass
class ConditionalExprNode(ExpressionNode):
    if_expr: 'ExpressionNode'
    then_expr: 'ExpressionNode'
    else_expr: 'ExpressionNode'
