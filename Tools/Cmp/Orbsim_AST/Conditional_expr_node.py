from ast import Expression
from dataclasses import dataclass



@dataclass
class ConditionalExprNode(Expression):
    if_expr: Expression
    then_expr: Expression
    else_expr: Expression