from dataclasses import dataclass
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
@dataclass
class AssingNode():
    var_id = str
    expr: 'ExpressionNode'