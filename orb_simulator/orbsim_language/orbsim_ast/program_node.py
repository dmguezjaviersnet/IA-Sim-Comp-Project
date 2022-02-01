from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.node import Node
from orbsim_language.orbsim_ast.statement_node import StatementNode
from orbsim_language.context import Context

__all__= ['ProgramNode']

@dataclass
class ProgramNode(Node):
    statements: List['StatementNode']

    def validate(self, context: 'Context'):
        for statement in self.statements:
            if not statement.validate(context):
                return False
        return True
  
    
