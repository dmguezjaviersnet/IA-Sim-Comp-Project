
from orbsim_ast.expression_node import ExpressionNode
from dataclasses import dataclass
from orbsim_ast.context import Context

@dataclass
class AtomicNode(ExpressionNode):
    val: str
    
    def validate(self, context: 'Context') -> bool:
        return True
    