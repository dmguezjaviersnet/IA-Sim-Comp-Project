from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
from dataclasses import dataclass

from Context import Context



@dataclass
class Variable_node(Expression_node):
    identifier: str

    def validate(self, context: Context):
        return context.check_var(self.identifier)