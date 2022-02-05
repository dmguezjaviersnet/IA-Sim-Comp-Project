from dataclasses import dataclass
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.orbsim_ast.assign_node import AssingNode
@dataclass
class AssingNode():
    var_id = str
    expr: 'ExpressionNode'