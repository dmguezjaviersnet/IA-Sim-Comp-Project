from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.node import Node
from orbsim_language.orbsim_ast.statement_node import StatementNode


__all__= ['ProgramNode']

@dataclass
class ProgramNode(Node):
    statements: List['StatementNode']
    
