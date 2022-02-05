from dataclasses import dataclass
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.context import Context

@dataclass
class VariableNode(ExpressionNode):
    identifier: str

    def validate(self, context: 'Context'):
        return context.check_var(self.identifier)