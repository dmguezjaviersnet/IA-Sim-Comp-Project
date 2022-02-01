import orbsim_language.visitor as visitor
from   orbsim_language.context import Context, Scope
from   orbsim_language.orbsim_ast.program_node import ProgramNode
from orbsim_language.orbsim_ast.func_declr_node import FuncDeclrNode
class TypeChecker:
    context: Context
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: 'Scope' = None):
        scope = Scope()
        for statement in node.statements:
            self.visit(statement, scope.create_child_scope())
        return scope

    @visitor.when(FuncDeclrNode)
    def visit(self, node: FuncDeclrNode, scope: 'Scope'):
        

    