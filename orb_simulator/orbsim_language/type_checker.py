import orbsim_language.visitor as visitor
from   orbsim_language.context import Context

class TypeChecker:
    context: Context
    @visitor.on('node')
    def visit(self, node):
        pass
    
    