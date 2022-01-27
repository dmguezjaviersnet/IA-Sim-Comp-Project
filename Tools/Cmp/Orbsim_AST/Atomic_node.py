
from Expression_node import Expression_node
from dataclasses import dataclass
from Context import Context

@dataclass
class Atomic_node('Expression_node'):
    val: str
    
    def validate(self, context: 'Context') -> bool:
        return True
    