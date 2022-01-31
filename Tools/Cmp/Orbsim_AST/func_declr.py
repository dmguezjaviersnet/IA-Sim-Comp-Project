from dataclasses import dataclass
from typing import List
from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
from Context import Context

__all__ = ['FuncDeclr']

@dataclass
class FuncDeclr(Expression_node):
    identifier: str
    args: List[str]
    body: 'Expression_node'

    def validate(self, context: 'Context') -> bool:
        inner_context = context.create_child_context()

        for arg in self.args:
            inner_context.define_var(arg)
        
        if  not self.body.validate(inner_context):
            return False
        
        return context.define_fun(self.identifier, self.args) 