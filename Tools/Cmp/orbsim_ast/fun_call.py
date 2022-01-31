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