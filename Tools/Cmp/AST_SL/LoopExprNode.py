
from dataclasses import dataclass

from ExpressionNode import ExpressionNode
@dataclass
class LoopExprNode(ExpressionNode):
    condition: ExpressionNode
    body: ExpressionNode

    
    