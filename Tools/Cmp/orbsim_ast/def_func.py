from dataclasses import dataclass
from typing import List
from orbsim_ast.expression_node import ExpressionNode
from orbsim_ast.context import Context

@dataclass
class DefFunc(ExpressionNode):
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