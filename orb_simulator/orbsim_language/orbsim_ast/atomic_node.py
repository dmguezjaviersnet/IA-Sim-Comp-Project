from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.context import Context
from dataclasses import dataclass

@dataclass
class AtomicNode(ExpressionNode):
    val: str
    
    def validate(self, context: 'Context') -> bool:
        return True
    