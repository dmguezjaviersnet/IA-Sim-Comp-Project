from typing import overload
from other_language.testing_ast.Expression import *

class BinaryExpression(Expression):



    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return self.left.__str__()  + self.right.__str__()
    
    
   