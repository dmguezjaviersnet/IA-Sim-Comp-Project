from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.orbsim_ast.statement_node import StatementNode

@dataclass
class LoopNode(StatementNode):
    condition: 'ExpressionNode'
    body: List['StatementNode']

    
    