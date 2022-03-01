from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.expression_node import ExpressionNode

@dataclass
class TupleCreationNode(ExpressionNode):
    elems: List[ExpressionNode]