
from ast import Expression
from dataclasses import dataclass
from Context import Context

@dataclass
class AtomicNode(Expression):
    val: str
    
    def validate(self, context: 'Context') -> bool:
        return True
    