

from dataclasses import dataclass
from Expression_node import ExpressionNode
from Statement_node import Statement_node
from Context import Context

@dataclass
class Let_variable(Statement_node):
    identifier: str
    expr: 'ExpressionNode'

    def validate(self, context: 'Context') -> bool:
        if not self.expr.validate(context):
            return False
        if not context.define_var(self.identifier):
            return False
        return True
