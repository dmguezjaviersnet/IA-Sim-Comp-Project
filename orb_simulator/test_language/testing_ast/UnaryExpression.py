from typing import overload
from test_language.testing_ast.Expression import Expression

class UnaryExpression(Expression):



    def __init__(self, exp: Expression):
        self.exp = exp
        
     
    
   