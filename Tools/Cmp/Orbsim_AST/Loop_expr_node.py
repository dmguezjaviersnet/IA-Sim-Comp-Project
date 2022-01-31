
from dataclasses import dataclass
from Tools.Cmp.Orbsim_AST.expression_node import Expression_node

@dataclass
class Loop_expr_node(Expression_node):
    condition: 'Expression_node'
    body: 'Expression_node'

    
    