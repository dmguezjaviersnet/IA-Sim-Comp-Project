from dataclasses import dataclass
from typing import List
from orbsim_ast.node import Node
from orbsim_ast.statement_node import StatementNode
from orbsim_ast.context import Context


@dataclass
class ProgramNode(Node):
    statements: List['StatementNode']

    def validate(self, context: 'Context'):
        for statement in self.statements:
            if not statement.validate(context):
                return False
        return True
  
    
