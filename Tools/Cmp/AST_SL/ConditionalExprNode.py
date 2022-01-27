from ast import Expression
from dataclasses import dataclass

from Tools.Cmp.AST_SL.ExpressionNode import Expression

@dataclass
class ConditionalExprNode(Expression):
    if_expr: Expression
    then_expr: Expression
    else_expr: Expression