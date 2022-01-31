<<<<<<< HEAD:Tools/Cmp/orbsim_ast/fun_call.py
=======
from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
>>>>>>> 8005a5681d7c4b95ae36a9eafaccac75544792c9:Tools/Cmp/Orbsim_AST/Fun_call.py
from dataclasses import dataclass
from typing import List
from orbsim_ast.expression_node import ExpressionNode
from orbsim_ast.context import Context



@dataclass
class FunCall:
    identifier: str
    args: List['ExpressionNode']

    def validate(self, context: 'Context') -> bool:
        for exp in self.args:
            if not exp.validate(context):
                return False
        return context.check_fun(self.identifier, len(self.args))