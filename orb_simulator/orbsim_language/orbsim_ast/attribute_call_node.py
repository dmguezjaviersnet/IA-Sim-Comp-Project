from dataclasses import dataclass
from orbsim_language.orbsim_ast.expression_node import ExpressionNode

@dataclass
class AttributeCallNode(ExpressionNode):
    instance_name: str
    identifier: str
    comp_type = None

   