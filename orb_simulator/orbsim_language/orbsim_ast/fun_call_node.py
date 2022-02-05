from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from dataclasses import dataclass
from typing import List

@dataclass
class FunCallNode(ExpressionNode):
    identifier: str
    args: List['ExpressionNode']

   