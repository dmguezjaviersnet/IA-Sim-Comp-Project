from typing import List
from   orbsim_language.orbsim_type import *
import orbsim_language.visitor as visitor
from   orbsim_language.context import Context, Scope
from   orbsim_language.orbsim_ast.program_node import ProgramNode
from   orbsim_language.orbsim_ast.func_declr_node import FuncDeclrNode
from   orbsim_language.orbsim_ast.variable_declr_node import VariableDeclrNode
from   orbsim_language.orbsim_ast.variable_node import VariableNode
from   orbsim_language.orbsim_ast.fun_call_node import FunCallNode
from   orbsim_language.orbsim_ast.plus_node import PlusNode
from   orbsim_language.orbsim_ast.string_node import StringNode
from   orbsim_language.orbsim_ast.integer_node import IntegerNode
from   orbsim_language.orbsim_ast.float_node import FloatNode
from   orbsim_language.orbsim_ast.boolean_node import BooleanNode

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
            self.visit(statement, scope)
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
            if not self.context.define_fun(node.identifier, fun_ret_type, node.args, arg_types):
                self.log(f'Ya está definida una función con nombre {node.identifier}')
        
        self.visit(node.body, scope.create_child_scope())
    
    @visitor.when(VariableDeclrNode)
    def visit(self, node: VariableDeclrNode, scope: 'Scope'):
        try:
            var_type = self.context.get_type(node.type) # dame el tipo si existe de esta variable en caso que esté definido en el context
            
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)
        
        if not scope.define_var(node.identifier, var_type, node.expr):
            self.log.append(f'SemanticError: Ya existe una variable definida con el nombre {node.identifier}')
            
        expr = self.visit(node.expr, scope)

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: 'Scope'):
        if not scope.check_var(node.identifier):
            self.log(f'SemanticError: La variable{node.identifier} no se encuentra definida en el programa')
        

    @visitor.when(FunCallNode)
    def visit(self, node: FunCallNode, scope: 'Scope'):
        if not self.context.check_fun(node.identifier, len(node.args)): # si existe una función definida con ese nombre y esa cantidad de parámetros
            self.log(f'SemanticError: No existe una función con nombre {node.identifier}')
    
    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: 'Scope'):
        self.visit(node.left)
        left_type: OrbsimType = node.comp_type
        self.visit(node.right)
        right_type: OrbsimType = node.comp_type
        if left_type != right_type or left_type.name != 'Int':
            self.log.append(f'SemanticError: La operación +  no está definida entre {left_type.name} y {right_type.name}')
        #node.comp_type =
    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: 'Scope'):
        node.comp_type = StringType()
    
    @visitor.when(IntegerNode)
    def visit(self, node: IntegerNode, scope: 'Scope'):
        node.comp_type = IntType()
    
    @visitor.when(FloatNode)
    def visit(self, node: FloatNode, scope: 'Scope'):
        node.comp_type = FloatType()
    
    @visitor.when(BooleanNode)
    def visit(self, node: BooleanNode, scope: 'Scope'):
        node.comp_type = BoolType()
    
    # @visitor.when()
       

    # @visitor.when()