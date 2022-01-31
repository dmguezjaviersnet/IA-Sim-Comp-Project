

from dataclasses import dataclass
from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
from Tools.Cmp.Orbsim_AST.statement_node import Statement_node
from Context import Context

@dataclass
class VariableDeclr(Statement_node):
    identifier: str
    expr: 'Expression_node'

    def validate(self, context: 'Context') -> bool:
        if not self.expr.validate(context):
            return False
        if not context.define_var(self.identifier):
            return False
        return True
