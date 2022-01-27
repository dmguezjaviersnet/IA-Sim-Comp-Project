from dataclasses import dataclass
from typing import List
from Node import Node
from StatementNode import StatementNode
from Context import Context


@dataclass
class ProgramNode(Node):
    statements: List['StatementNode']

    def validate(self, context: 'Context'):
        for statement in self.statements:
            if not statement.validate(context):
                return False
        return True
  
    
