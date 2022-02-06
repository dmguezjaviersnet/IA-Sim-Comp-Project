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
    

    def __init__(self, context: Context =Context(), log: List[str] = []):
        self.context: Context = context
        self.log: List[str]   = context
        
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
        try:
            fun_ret_type = self.context.get_type(node.return_type)
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)
        
        arg_types = []
        for t in node.arg_types:
            try:
                arg_type = self.context.get_type(t)
                arg_types.append(arg_type)
            except OrbisimSemanticError as err:
                self.log(err.error_info)
        if len(arg_types) == len(node.arg_types):
            if not scope.define_fun(node.identifier, fun_ret_type, node.args, arg_types):
                self.log(f'Ya está definida una función con nombre {node.identifier}')

        for st in node.body:
            self.visit(st, scope.create_child_scope())
    
    @visitor.when(VariableDeclrNode)
    def visit(self, node: VariableDeclrNode, scope: 'Scope'):
        try:
            var_type = self.context.get_type(node.type) # dame el tipo si existe de esta variable en caso que esté definido en el context
            
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)
        
        if not scope.define_var(node.identifier, var_type, node.expr):
            self.log.append(f'SemanticError: Ya existe una variable definida con el nombre {node.identifier}')
            
        self.visit(node.expr, scope)

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: 'Scope'):
        if not scope.check_var(node.identifier):
            self.log(f'SemanticError: La variable{node.identifier} no se encuentra definida en el programa')
        

    @visitor.when(FunCallNode)
    def visit(self, node: FunCallNode, scope: 'Scope'):
        if not scope.check_fun(node.identifier, len(node.args)): # si existe una función definida con ese nombre y esa cantidad de parámetros
            self.log(f'SemanticError: No existe una función con nombre {node.identifier}')
    
    # @visitor.when()
       

    # @visitor.when()