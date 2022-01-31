from dataclasses import dataclass
from typing import List
<<<<<<< HEAD:Tools/Cmp/orbsim_ast/program_node.py
from orbsim_ast.node import Node
from orbsim_ast.statement_node import StatementNode
from orbsim_ast.context import Context
=======
from Node import Node
from Tools.Cmp.Orbsim_AST.statement_node import Statement_node
from Context import Context
>>>>>>> 8005a5681d7c4b95ae36a9eafaccac75544792c9:Tools/Cmp/Orbsim_AST/program_node.py


__all__= ['ProgramNode']

@dataclass
class ProgramNode(Node):
<<<<<<< HEAD:Tools/Cmp/orbsim_ast/program_node.py
    statements: List['StatementNode']
=======
    statements: List['Statement_node']
>>>>>>> 8005a5681d7c4b95ae36a9eafaccac75544792c9:Tools/Cmp/Orbsim_AST/program_node.py

    def validate(self, context: 'Context'):
        for statement in self.statements:
            if not statement.validate(context):
                return False
        return True
  
    
