
from dataclasses import dataclass
from expression_node import ExpressionNode
from statement_node import StatementNode

@dataclass
class AttributeDef(StatementNode):
    name: str
    type: str
    init: ExpressionNode