
from ast import Expression
from dataclasses import dataclass

from Context import Context



@dataclass
class VariableNode(Expression):
    identifier: str

    def validate(self, context: Context):
        return context.check_var(self.identifier)