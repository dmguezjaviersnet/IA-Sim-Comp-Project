from typing import overload
from Expression import *

class UnaryExpression(Expression):



    def __init__(self, exp: Expression):
        self.exp = exp
        
     
    
   