from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.orbsim_ast.statement_node import StatementNode
from orbsim_language.orbsim_ast.body_node import BodyNode
@dataclass
class LoopNode(StatementNode):
    condition: 'ExpressionNode'
    body: BodyNode

    
    