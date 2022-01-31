from dataclasses import dataclass
from typing import List
<<<<<<<< HEAD:Tools/Cmp/orbsim_ast/def_func.py
from orbsim_ast.expression_node import ExpressionNode
from orbsim_ast.context import Context
========
from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
from Context import Context
>>>>>>>> 8005a5681d7c4b95ae36a9eafaccac75544792c9:Tools/Cmp/orbsim_ast/func_declr.py

__all__ = ['FuncDeclr']

@dataclass
<<<<<<<< HEAD:Tools/Cmp/orbsim_ast/def_func.py
class DefFunc(ExpressionNode):
========
class FuncDeclr(Expression_node):
>>>>>>>> 8005a5681d7c4b95ae36a9eafaccac75544792c9:Tools/Cmp/orbsim_ast/func_declr.py
    identifier: str
    args: List[str]
    body: 'ExpressionNode'

    def validate(self, context: 'Context') -> bool:
        inner_context = context.create_child_context()

        for arg in self.args:
            inner_context.define_var(arg)
        
        if  not self.body.validate(inner_context):
            return False
        
        return context.define_fun(self.identifier, self.args) 