from typing import List
from   orbsim_language.orbsim_type import *
import orbsim_language.visitor as visitor
from   orbsim_language.context import Context, FunctionInfo, Scope, VariableInfo
from   orbsim_language.orbsim_ast.program_node import ProgramNode
from   orbsim_language.orbsim_ast.func_declr_node import FuncDeclrNode
from   orbsim_language.orbsim_ast.variable_declr_node import VariableDeclrNode
from   orbsim_language.orbsim_ast.variable_node import VariableNode
from   orbsim_language.orbsim_ast.fun_call_node import FunCallNode
from   orbsim_language.orbsim_ast.plus_node import PlusNode
from   orbsim_language.orbsim_ast.minus_node import MinusNode
from   orbsim_language.orbsim_ast.product_node import ProductNode
from   orbsim_language.orbsim_ast.div_node import DivNode
from   orbsim_language.orbsim_ast.mod_node import ModNode
from   orbsim_language.orbsim_ast.string_node import StringNode
from   orbsim_language.orbsim_ast.integer_node import IntegerNode
from   orbsim_language.orbsim_ast.float_node import FloatNode
from   orbsim_language.orbsim_ast.boolean_node import BooleanNode
from   orbsim_language.orbsim_ast.and_node import AndNode
from   orbsim_language.orbsim_ast.or_node import OrNode
from   orbsim_language.orbsim_ast.not_node import NotNode
from   orbsim_language.orbsim_ast.bitwise_and_node import BitwiseAndNode
from   orbsim_language.orbsim_ast.bitwise_or_node import BitwiseOrNode
from   orbsim_language.orbsim_ast.bitwise_xor_node import BitwiseXorNode
from   orbsim_language.orbsim_ast.bitwise_shift_left_node import BitwiseShiftLeftNode
from   orbsim_language.orbsim_ast.bitwise_shift_right_node import BitwiseShiftRightNode

from errors import OrbisimSemanticError
class TypeChecker:
    

    def __init__(self, context: Context =Context(), log: List[str] = []):
        self.context: Context = context
        self.log: List[str]   = log
        
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
            var_type: OrbsimType = self.context.get_type(node.type) # dame el tipo si existe de esta variable en caso que esté definido en el context
            
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)
        
        if not scope.define_var(node.identifier, var_type, node.expr):
            self.log.append(f'SemanticError: Ya existe una variable definida con el nombre {node.identifier}')
            
        self.visit(node.expr, scope)
        
        if  node.expr.comp_type != var_type:
            self.log.append(f'SemanticError: No se puede asignar una expresión de tipo {node.expr.comp_type.name} a la variable {node.identifier}  de tipo {var_type.name}')
    
    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: 'Scope'):
        if not scope.check_var(node.identifier):
            node.comp_type = NullType()
            self.log(f'SemanticError: La variable{node.identifier} no se encuentra definida en el programa')
        else:
            var: 'VariableInfo' = scope.get_variable(node.identifier)
            node.comp_type = var.type
    
    @visitor.when(FunCallNode)
    def visit(self, node: FunCallNode, scope: 'Scope'):
        if not self.context.check_fun(node.identifier, len(node.args)): # si existe una función definida con ese nombre y esa cantidad de parámetros
            node.comp_type = NullType()
            self.log(f'SemanticError: No existe una función con nombre {node.identifier}')
        else:
            func: 'FunctionInfo' = self.context.get_func(node.identifier, len(node.args))
            node.comp_type = func.return_type
            
    
    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int' or left_type.name != 'Float':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación +  no está definida entre {left_type.name} y {right_type.name}')
        else:
            if left_type.name == 'Int':
                node.comp_type = IntType() 
            else:
                node.comp_type = FloatType()
    
    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int' or left_type.name != 'Float':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación -  no está definida entre {left_type.name} y {right_type.name}')
        else:
            if left_type.name == 'Int':
                node.comp_type = IntType() 
            else:
                node.comp_type = FloatType()
    
    @visitor.when(DivNode)
    def visit(self, node: DivNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int' or left_type.name != 'Float':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación /  no está definida entre {left_type.name} y {right_type.name}')
        else:
            if left_type.name == 'Int':
                node.comp_type = IntType() 
            else:
                node.comp_type = FloatType()
    
    @visitor.when(ProductNode)
    def visit(self, node: ProductNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int' or left_type.name != 'Float':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación *  no está definida entre {left_type.name} y {right_type.name}')
        else:
            if left_type.name == 'Int':
                node.comp_type = IntType() 
            else:
                node.comp_type = FloatType()
    
    @visitor.when(ModNode)
    def visit(self, node: ModNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación %  no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = IntType() 
    
    @visitor.when(AndNode)
    def visit(self, node: AndNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Bool':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación && no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = BoolType() 

    @visitor.when(OrNode)
    def visit(self, node: OrNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Bool':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación || no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = BoolType() 

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: 'Scope'):
        self.visit(node.expr, scope)
        expr_type: OrbsimType = node.expr.comp_type
        
        if expr_type.name != 'Bool':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación not no está definida para el tipo {expr_type.name}')
        else:
            node.comp_type = BoolType() 

    @visitor.when(BitwiseAndNode)
    def visit(self, node: BitwiseAndNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise and & no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 

    @visitor.when(BitwiseOrNode)
    def visit(self, node: BitwiseOrNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise or |  no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 

    @visitor.when(BitwiseXorNode)
    def visit(self, node: BitwiseXorNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise xor ^ no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 

    @visitor.when(BitwiseShiftRightNode)
    def visit(self, node: BitwiseShiftRightNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise shift right  >> no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 
    
    @visitor.when(BitwiseShiftLeftNode)
    def visit(self, node: BitwiseShiftLeftNode, scope: 'Scope'):
        self.visit(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.visit(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise shift left  << no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 


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
    
    