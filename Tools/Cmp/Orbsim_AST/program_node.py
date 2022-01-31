from dataclasses import dataclass
from typing import List
from Node import Node
from Tools.Cmp.Orbsim_AST.statement_node import Statement_node
from Context import Context


__all__= ['ProgramNode']

@dataclass
class ProgramNode(Node):
    statements: List['Statement_node']

    def validate(self, context: 'Context'):
        for statement in self.statements:
            if not statement.validate(context):
                return False
        return True
  
    
