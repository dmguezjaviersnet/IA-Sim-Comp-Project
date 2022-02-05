from dataclasses import dataclass
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.orbsim_ast.statement_node import StatementNode
from orbsim_language.context import Context

@dataclass
class VariableDeclrNode(StatementNode):
    identifier: str
    type: str
    expr: 'ExpressionNode'
    

    def validate(self, context: 'Context') -> bool:
        if not self.expr.validate(context):
            return False
        if not context.define_var(self.identifier):
            return False
        return True
