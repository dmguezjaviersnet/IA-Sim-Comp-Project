from Expression import *

class Number(Expression):

    def __init__(self, val: int):
        self.val = val;
    
    def eval(self):
        return self.val;

    
  