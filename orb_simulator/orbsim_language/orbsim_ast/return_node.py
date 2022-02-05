from pathy import dataclass
from orbsim_language.orbsim_ast.expression_node import ExpressionNode

@dataclass
class ReturnNode(ExpressionNode):
    expr: 'ExpressionNode'
