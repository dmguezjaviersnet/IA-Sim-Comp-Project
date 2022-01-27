

from dataclasses import dataclass
from ExpressionNode import ExpressionNode
from StatementNode import StatementNode
from Context import Context

@dataclass
class LetVariable(StatementNode):
    identifier: str
    expr: 'ExpressionNode'

    def validate(self, context: 'Context') -> bool:
        if not self.expr.validate(context):
            return False
        if not context.define_var(self.identifier):
            return False
        return True
