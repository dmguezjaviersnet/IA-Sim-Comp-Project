from dataclasses import dataclass
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.orbsim_ast.statement_node import StatementNode

@dataclass
class VariableDeclrNode(StatementNode):
    identifier: str
    type: str
    expr: 'ExpressionNode'