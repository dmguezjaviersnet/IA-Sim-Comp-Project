from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.statement_node import StatementNode
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.orbsim_ast.body_node import BodyNode

@dataclass
class MethodDeclrNode(StatementNode):
    name: str
    return_type: str
    arg_names = List[str]
    arg_types = List[str]
    body: BodyNode

