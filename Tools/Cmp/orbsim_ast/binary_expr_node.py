from dataclasses import dataclass
from orbsim_ast.expression_node import ExpressionNode

@dataclass
class BinaryExprNode(ExpressionNode):
    left: 'ExpressionNode'
    right:'ExpressionNode'
    operator: str