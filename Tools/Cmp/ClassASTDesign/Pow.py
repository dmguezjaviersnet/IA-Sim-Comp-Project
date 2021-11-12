from BinaryExpression import *

class Pow(BinaryExpression):
    
    def __init__(self, left: Expression, right: Expression):
       super().__init__(left, right)
    
    def eval(self):
        self.left.eval() * self.right.eval()
    
        

    
        