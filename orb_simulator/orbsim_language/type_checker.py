from typing import List
import orbsim_language.visitor as visitor
from   orbsim_language.context import Context, Scope
from   orbsim_language.orbsim_ast.program_node import ProgramNode
from   orbsim_language.orbsim_ast.func_declr_node import FuncDeclrNode
from   orbsim_language.orbsim_ast.variable_declr_node import VariableDeclrNode
from   orbsim_language.orbsim_ast.variable_node import VariableNode
from   orbsim_language.orbsim_ast.fun_call_node import FunCallNode
from errors import OrbisimSemanticError
class TypeChecker:
    context: Context
    log: List[str]
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
        try:
            var_type = self.context.get_type(node.type) # dame el tipo si existe de esta variable
            
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)
        
        if not scope.define_var(node.identifier, var_type, node.expr):
            self.log.append(f'Ya existe una variable definida con el nombre {node.identifier}')
            
        self.visit(node.expr, scope)

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: 'Scope'):
        if not scope.check_var(node.identifier):
            self.log(f'La variable{node.identifier} no se encuentra definida en el programa')
        

    @visitor.when(FunCallNode)
    def visit(self, node: FunCallNode, scope: 'Scope'):
        if not scope.check_fun(node.identifier, len(node.args)): # si existe una función definida con ese nombre y esa cantidad de parámetros
            ...

    # @visitor.when()