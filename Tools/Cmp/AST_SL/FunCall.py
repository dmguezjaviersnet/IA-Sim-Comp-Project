from ExpressionNode import ExpressionNode
from dataclasses import dataclass
from typing import List
from Context import Context



@dataclass
class FunCall:
    identifier: str
    args: List[ExpressionNode]

    def validate(self, context: 'Context') -> bool:
        for exp in self.args:
            if not exp.validate(context):
                return False
        return context.check_fun(self.identifier, len(self.args))