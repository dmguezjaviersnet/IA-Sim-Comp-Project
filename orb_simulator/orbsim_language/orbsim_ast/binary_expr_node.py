from dataclasses import dataclass
from orbsim_language.orbsim_ast.expression_node import ExpressionNode

@dataclass
class BinaryExprNode(ExpressionNode):
    left: 'ExpressionNode'
    right: 'ExpressionNode'
    comp_type = None
