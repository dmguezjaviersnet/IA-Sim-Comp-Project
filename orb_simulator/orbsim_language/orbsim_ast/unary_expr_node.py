from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from dataclasses import dataclass

@dataclass
class UnaryExprNode(ExpressionNode):
    expr: 'ExpressionNode'
    comp_type =  None
