from dataclasses import dataclass
from orbsim_language.orbsim_ast.expression_node import ExpressionNode

@dataclass
class VariableNode(ExpressionNode):
    identifier: str

   