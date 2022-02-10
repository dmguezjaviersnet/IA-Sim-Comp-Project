from typing import List
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from dataclasses import dataclass

@dataclass
class MethodCallNode(ExpressionNode):
    instance_name: str
    identifier: str
    args: List['ExpressionNode']
    comp_type = None

