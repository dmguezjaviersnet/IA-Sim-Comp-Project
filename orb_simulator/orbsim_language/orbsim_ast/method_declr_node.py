from typing import List
from orbsim_language.orbsim_ast.statement_node import StatementNode
from orbsim_language.orbsim_ast.expression_node import ExpressionNode

class MethodDeclrNode(StatementNode):
    name: str
    return_type: str
    arg_names = List[str]
    arg_types = List[str]
    body: 'ExpressionNode'

