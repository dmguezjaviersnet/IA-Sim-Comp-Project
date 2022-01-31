from typing import overload
from testing_ast.UnaryExpression import *

class Not(UnaryExpression):

    def __init__(self, exp: Expression):
        super().__init__(exp)
    
    def eval(self):
        not self.exp.eval()   
    
    
   