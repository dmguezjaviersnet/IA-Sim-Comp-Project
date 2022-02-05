from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.orbsim_ast.statement_node import StatementNode

__all__ = ['FuncDeclrNode']

@dataclass
class FuncDeclrNode(StatementNode):
    identifier: str
    type: str
    args: List[str]
    body: List['StatementNode']

  