from typing import List
from orbsim_language.orbsim_ast.statement_node import StatementNode
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from dataclasses import dataclass

@dataclass
class ConditionalNode(StatementNode):
    if_expr: 'ExpressionNode'
    then_expr: List['StatementNode']
    else_expr: List['StatementNode']
