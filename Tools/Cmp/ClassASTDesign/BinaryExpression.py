from typing import overload
from Expression import *

class BinaryExpression(Expression):



    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    
   