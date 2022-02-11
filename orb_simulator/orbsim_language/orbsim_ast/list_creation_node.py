from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.expression_node import ExpressionNode

@dataclass
class ListCreationNode(ExpressionNode):
    elems: List[ExpressionNode]