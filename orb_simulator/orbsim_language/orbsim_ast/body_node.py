from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.statement_node import StatementNode

@dataclass
class BodyNode(StatementNode):
    statements: List[StatementNode]

