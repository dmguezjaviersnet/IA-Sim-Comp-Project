import orbsim_language.visitor as visitor
from   orbsim_language.context import Context, Scope
from   orbsim_language.orbsim_ast import ProgramNode
from   orbsim_language.orbsim_ast import FuncDeclrNode
from   orbsim_language.orbsim_ast import VariableDeclrNode
from   orbsim_language.orbsim_ast import VariableNode
from   orbsim_language.orbsim_ast import FunCallNode
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
        scope.define_fun(node.identifier, len(node.args))
        for st in node.body:
            self.visit(st, scope)
    
    @visitor.when(VariableDeclrNode)
    def visit(self, node: VariableDeclrNode, scope: 'Scope'):
        scope.define_var(node.identifier)
        self.visit(node.expr, scope)

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: 'Scope'):
        if not scope.check_var(node.identifier):
            ...

    @visitor.when(FunCallNode)
    def visit(self, node: FunCallNode, scope: 'Scope'):
        if not scope.check_fun(node.identifier, len(node.args)): # si existe una función definida con ese nombre y esa cantidad de parámetros
            ...

    # @visitor.when()