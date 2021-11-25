from ClassASTDesign.BinaryExpression import *

class Sum(BinaryExpression):
    
    def __init__(self, left: Expression, right: Expression):
       super().__init__(left, right)
    
    def eval(self):
        self.left.eval() + self.right.eval()
    
        

    
        