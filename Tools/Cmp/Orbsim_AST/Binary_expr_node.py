from dataclasses import dataclass
from Expression_node import Expression_node

@dataclass
class Binary_expr_node(Expression_node):
    left: 'Expression_node'
    right:'Expression_node'
    operator: str