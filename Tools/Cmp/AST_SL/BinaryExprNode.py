
from ast import Expression
from dataclasses import dataclass
from turtle import right


@dataclass
class BinaryExprNode(Expression):
    left: Expression
    right:Expression
    operator: str