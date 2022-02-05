from test_language.testing_ast.Expression import *

class Number(Expression):

    def __init__(self, val: int):
        self.val = val;
    
    def eval(self):
        return self.val;

    def __str__(self) -> str:
        return str(self.val)

    
  