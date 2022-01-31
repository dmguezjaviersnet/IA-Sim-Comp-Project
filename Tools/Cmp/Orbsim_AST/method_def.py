from typing import List
from statement_node import StatementNode
from expression_node import ExpressionNode

class MethodDef(StatementNode):
    name: str
    return_type: str
    arg_names = List[str]
    arg_types = List[str]
    body: ExpressionNode

