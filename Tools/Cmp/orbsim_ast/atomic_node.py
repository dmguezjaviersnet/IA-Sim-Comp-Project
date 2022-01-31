
<<<<<<< HEAD:Tools/Cmp/orbsim_ast/atomic_node.py
from orbsim_ast.expression_node import ExpressionNode
=======
from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
>>>>>>> 8005a5681d7c4b95ae36a9eafaccac75544792c9:Tools/Cmp/Orbsim_AST/Atomic_node.py
from dataclasses import dataclass
from orbsim_ast.context import Context

@dataclass
<<<<<<< HEAD:Tools/Cmp/orbsim_ast/atomic_node.py
class AtomicNode(ExpressionNode):
=======
class Atomic_node(Expression_node):
>>>>>>> 8005a5681d7c4b95ae36a9eafaccac75544792c9:Tools/Cmp/Orbsim_AST/Atomic_node.py
    val: str
    
    def validate(self, context: 'Context') -> bool:
        return True
    