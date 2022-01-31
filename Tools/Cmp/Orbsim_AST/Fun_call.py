from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
from dataclasses import dataclass
from typing import List
from Context import Context



@dataclass
class Fun_call:
    identifier: str
    args: List['Expression_node']

    def validate(self, context: 'Context') -> bool:
        for exp in self.args:
            if not exp.validate(context):
                return False
        return context.check_fun(self.identifier, len(self.args))