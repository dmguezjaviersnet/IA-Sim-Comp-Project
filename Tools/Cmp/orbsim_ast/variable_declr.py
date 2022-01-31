from dataclasses import dataclass
<<<<<<<< HEAD:Tools/Cmp/orbsim_ast/let_variable.py
from orbsim_ast.expression_node import ExpressionNode
from orbsim_ast.statement_node import StatementNode
from orbsim_ast.context import Context

@dataclass
class LetVariable(StatementNode):
========
from Tools.Cmp.Orbsim_AST.expression_node import Expression_node
from Tools.Cmp.Orbsim_AST.statement_node import Statement_node
from Context import Context

@dataclass
class VariableDeclr(Statement_node):
>>>>>>>> 8005a5681d7c4b95ae36a9eafaccac75544792c9:Tools/Cmp/orbsim_ast/variable_declr.py
    identifier: str
    expr: 'Expression_node'

    def validate(self, context: 'Context') -> bool:
        if not self.expr.validate(context):
            return False
        if not context.define_var(self.identifier):
            return False
        return True
