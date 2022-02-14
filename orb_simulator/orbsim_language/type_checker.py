from typing import List

from   orbsim_language.orbsim_type import *
import orbsim_language.visitor as visitor
from orbsim_language.orbsim_ast.method_declr_node import MethodDeclrNode
from orbsim_language.context import Context, FunctionInfo, Scope, VariableInfo
from orbsim_language.orbsim_ast.program_node import ProgramNode
from orbsim_language.orbsim_ast.func_declr_node import FuncDeclrNode
from orbsim_language.orbsim_ast.variable_declr_node import VariableDeclrNode
from orbsim_language.orbsim_ast.variable_node import VariableNode
from orbsim_language.orbsim_ast.fun_call_node import FunCallNode
from orbsim_language.orbsim_ast.plus_node import PlusNode
from orbsim_language.orbsim_ast.minus_node import MinusNode
from orbsim_language.orbsim_ast.product_node import ProductNode
from orbsim_language.orbsim_ast.div_node import DivNode
from orbsim_language.orbsim_ast.mod_node import ModNode
from orbsim_language.orbsim_ast.string_node import StringNode
from orbsim_language.orbsim_ast.integer_node import IntegerNode
from orbsim_language.orbsim_ast.float_node import FloatNode
from orbsim_language.orbsim_ast.boolean_node import BooleanNode
from orbsim_language.orbsim_ast.and_node import AndNode
from orbsim_language.orbsim_ast.or_node import OrNode
from orbsim_language.orbsim_ast.not_node import NotNode
from orbsim_language.orbsim_ast.bitwise_and_node import BitwiseAndNode
from orbsim_language.orbsim_ast.bitwise_or_node import BitwiseOrNode
from orbsim_language.orbsim_ast.bitwise_xor_node import BitwiseXorNode
from orbsim_language.orbsim_ast.bitwise_shift_left_node import BitwiseShiftLeftNode
from orbsim_language.orbsim_ast.bitwise_shift_right_node import BitwiseShiftRightNode
from orbsim_language.orbsim_ast.equal_node import EqualNode
from orbsim_language.orbsim_ast.not_equal_node import NotEqualNode
from orbsim_language.orbsim_ast.greater_than_node import GreaterThanNode
from orbsim_language.orbsim_ast.greater_equal_node import GreaterEqualNode
from orbsim_language.orbsim_ast.less_than_node import LessThanNode
from orbsim_language.orbsim_ast.less_equal_node import LessEqualNode
from orbsim_language.orbsim_ast.print_node import PrintNode
from orbsim_language.orbsim_ast.assign_node import AssingNode
from orbsim_language.orbsim_ast.loop_node import LoopNode
from orbsim_language.orbsim_ast.conditional_node import ConditionalNode
from orbsim_language.orbsim_ast.body_node import BodyNode
from orbsim_language.orbsim_ast.attribute_call_node import AttributeCallNode
from orbsim_language.orbsim_ast.class_make_node import ClassMakeNode
from orbsim_language.orbsim_ast.method_call_node import MethodCallNode
from orbsim_language.orbsim_ast.class_declr_node import ClassDeclrNode
from orbsim_language.orbsim_ast.list_creation_node import ListCreationNode
from orbsim_language.orbsim_ast.break_node import BreakNode
from orbsim_language.orbsim_ast.continue_node import ContinueNode

from errors import OrbisimSemanticError
class TypeChecker:
    

    def __init__(self, context: Context =Context(), log: List[str] = []):
        self.context: Context = context
        self.log: List[str]   = log
        self.current_type: 'OrbsimType' = None
        self.insine_loop = False
        
    @visitor.on('node')
    def check(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def check(self, node: ProgramNode, scope: 'Scope' = None):
        scope = Scope()
        for statement in node.statements:
            self.check(statement, scope)
        return scope

    @visitor.when(ClassDeclrNode)
    def check(self, node: ClassDeclrNode, scope: 'Scope'):
        self.current_type = self.context.get_type(node.name)

        for attr in node.attributes:
            self.check(attr, scope)
        
        for method in node.methods:
            self.check(method, scope)
    
    @visitor.when(MethodDeclrNode)
    def check(self, node: MethodDeclrNode, scope: 'Scope'):
        self.current_type.get_method(node.name, len(node.arg_names)).body = node.body
        self.check(node.body, scope.create_child_scope())


    @visitor.when(FuncDeclrNode)
    def check(self, node: FuncDeclrNode, scope: 'Scope'):
        try:
            fun_ret_type = self.context.get_type(node.return_type)
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)
        
        arg_types = []
        new_scope = Scope()
        for index_arg, t in enumerate(node.arg_types):
            try:
                arg_type = self.context.get_type(t)
                arg_types.append(arg_type)
                new_scope.define_var(node.args[index_arg], arg_type)
            except OrbisimSemanticError as err:
                self.log(err.error_info)
        if len(arg_types) == len(node.arg_types):
            if not self.context.define_fun(node.identifier, fun_ret_type, node.args, arg_types):
                self.log(f'Ya está definida una función con nombre {node.identifier}')
        else:
            
            self.check(node.body, new_scope)
    
    @visitor.when(VariableDeclrNode)
    def check(self, node: VariableDeclrNode, scope: 'Scope'):
        try:
            var_type: OrbsimType = self.context.get_type(node.type) # dame el tipo si existe de esta variable en caso que esté definido en el context
            
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)
            return
        
        if not scope.define_var(node.identifier, var_type):
            self.log.append(f'SemanticError: Ya existe una variable definida con el nombre {node.identifier}')
            
        self.check(node.expr, scope)
        
        if  node.expr.comp_type != var_type:
            self.log.append(f'SemanticError: No se puede asignar una expresión de tipo {node.expr.comp_type.name} a la variable {node.identifier}  de tipo {var_type.name}')
    
    @visitor.when(VariableNode)
    def check(self, node: VariableNode, scope: 'Scope'):
        if not scope.check_var(node.identifier):
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La variable{node.identifier} no se encuentra definida en el programa')
        else:
            var: 'VariableInfo' = scope.get_variable(node.identifier)
            node.comp_type = var.type
    
    @visitor.when(FunCallNode)
    def check(self, node: FunCallNode, scope: 'Scope'):
        if not self.context.check_fun(node.identifier, len(node.args)): # si existe una función definida con ese nombre y esa cantidad de parámetros
            node.comp_type = NullType()
            self.log(f'SemanticError: No existe una función con nombre {node.identifier}')
        else:
            func: 'FunctionInfo' = self.context.get_func(node.identifier, len(node.args))
            node.comp_type = func.return_type
            
    
    @visitor.when(PlusNode)
    def check(self, node: PlusNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int' and left_type.name != 'Float':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación +  no está definida entre {left_type.name} y {right_type.name}')
        else:
            if left_type.name == 'Int':
                node.comp_type = IntType() 
            else:
                node.comp_type = FloatType()
    
    @visitor.when(MinusNode)
    def check(self, node: MinusNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int' and left_type.name != 'Float':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación -  no está definida entre {left_type.name} y {right_type.name}')
        else:
            if left_type.name == 'Int':
                node.comp_type = IntType() 
            else:
                node.comp_type = FloatType()
    
    @visitor.when(DivNode)
    def check(self, node: DivNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int' and left_type.name != 'Float':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación /  no está definida entre {left_type.name} y {right_type.name}')
        else:
            if left_type.name == 'Int':
                node.comp_type = IntType() 
            else:
                node.comp_type = FloatType()
    
    @visitor.when(ProductNode)
    def check(self, node: ProductNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int' and left_type.name != 'Float':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación *  no está definida entre {left_type.name} y {right_type.name}')
        else:
            if left_type.name == 'Int':
                node.comp_type = IntType() 
            else:
                node.comp_type = FloatType()
    
    @visitor.when(ModNode)
    def check(self, node: ModNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación %  no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = IntType() 
    
    @visitor.when(AndNode)
    def check(self, node: AndNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Bool':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación && no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = BoolType() 

    @visitor.when(OrNode)
    def check(self, node: OrNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Bool':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación || no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = BoolType() 

    @visitor.when(NotNode)
    def check(self, node: NotNode, scope: 'Scope'):
        self.check(node.expr, scope)
        expr_type: OrbsimType = node.expr.comp_type
        
        if expr_type.name != 'Bool':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación not no está definida para el tipo {expr_type.name}')
        else:
            node.comp_type = BoolType() 

    @visitor.when(BitwiseAndNode)
    def check(self, node: BitwiseAndNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise and & no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 

    @visitor.when(BitwiseOrNode)
    def check(self, node: BitwiseOrNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise or |  no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 

    @visitor.when(BitwiseXorNode)
    def check(self, node: BitwiseXorNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise xor ^ no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 

    @visitor.when(BitwiseShiftRightNode)
    def check(self, node: BitwiseShiftRightNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise shift right  >> no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 
    
    @visitor.when(BitwiseShiftLeftNode)
    def check(self, node: BitwiseShiftLeftNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or left_type.name != 'Int':
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación bitwise shift left  << no está definida entre {left_type.name} y {right_type.name}.\n La operacions lógicas bitwise solo está definida para los enteros.')
        else:
            node.comp_type = IntType() 


    @visitor.when(EqualNode)
    def check(self, node: EqualNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        node.comp_type = BoolType() 
    
    @visitor.when(NotEqualNode)
    def check(self, node: NotEqualNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        node.comp_type = BoolType() 

    @visitor.when(GreaterThanNode)
    def check(self, node: GreaterThanNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or (left_type.name != 'Int' and left_type.name != 'Float'):
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación > no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = BoolType() 
    
    @visitor.when(GreaterEqualNode)
    def check(self, node: GreaterEqualNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or (left_type.name != 'Int' and left_type.name != 'Float'):
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación >= no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = BoolType() 
    
    @visitor.when(LessThanNode)
    def check(self, node: LessThanNode, scope: 'Scope'):
        self.check(node.left, scope)
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or (left_type.name != 'Int' and left_type.name != 'Float'):
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación < no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = BoolType() 

    @visitor.when(LessEqualNode)
    def check(self, node: LessEqualNode, scope: 'Scope'):
        left_type: OrbsimType = node.left.comp_type
        self.check(node.right, scope)
        right_type: OrbsimType = node.right.comp_type
        if left_type != right_type or (left_type.name != 'Int' and left_type.name != 'Float'):
            node.comp_type = NullType()
            self.log.append(f'SemanticError: La operación <= no está definida entre {left_type.name} y {right_type.name}')
        else:
            node.comp_type = BoolType() 


    @visitor.when(PrintNode)
    def check(self, node: PrintNode, scope: 'Scope'):
        self.check(node.expr, scope)
        expr_type: OrbsimType =  node.expr.comp_type
        # if expr_type.name != 'Int' and expr_type.name != 'Float' and expr_type.name != 'Bool' and expr_type.name != 'String' and expr_type.name != 'Vector3':
        #     self.log.append(f'SemanticError: print no admite expresiones de tipo {expr_type.name}')
        
    @visitor.when(AssingNode)
    def check(self, node: AssingNode, scope: 'Scope'):
        self.check(node.expr, scope)
        if not scope.check_var(node.var_id):
            self.log.append(f'SemanticError: No existe una variable definida con nombre {node.var_id}')
        else:
            var_info: VariableInfo = scope.get_variable(node.var_id)
            if node.expr.comp_type != var_info.type:
                self.log.append(f'SemanticError: No le puedes asignar a una variable de tipo  {var_info.type} una expresión de tipo {node.expr.comp_type}')

    @visitor.when(ConditionalNode)
    def check(self, node: ConditionalNode, scope: 'Scope'):
        self.check(node.if_expr, scope)
        if_cond_type: OrbsimType =  node.if_expr.comp_type 
        if if_cond_type.name != 'Bool':
            self.log.append(f'SemanticError: Se esperaba una expresión de tipo Bool en la condición del if')
        self.check(node.then_expr, scope.create_child_scope())
        self.check(node.else_expr, scope.create_child_scope())

    @visitor.when(LoopNode)
    def check(self, node: LoopNode, scope: 'Scope'):
        self.check(node.condition, scope)
        condition_type: OrbsimType =  node.condition.comp_type 
        if condition_type.name != 'Bool':
            self.log.append(f'SemanticError: Se esperaba una expresión de tipo Bool en la condición del loop')
        self.insine_loop = True
        self.check(node.body, scope.create_child_scope())
        self.insine_loop = False

    @visitor.when(BodyNode)
    def check(self, node: BodyNode, scope: 'Scope'):
        for st in node.statements:
            if isinstance(st, ContinueNode) and not self.insine_loop:
                self.log('SemanticError: continue debe estar dentro de un loop')
            if isinstance(st, BreakNode) and not self.insine_loop:
                self.log('SemanticError: break debe estar dentro de un loop')
            self.check(st, scope)

    @visitor.when(AttributeCallNode)
    def check(self, node: AttributeCallNode, scope: 'Scope'):   
        if not scope.check_var(node.instance_name):
            node.comp_type = NullType()
            self.log(f'SemanticError: El nombre {node.instance_name} no está definido')
        else:
            var_instance: VariableInfo = scope.get_variable(node.instance_name)
            var_type = var_instance.type
            try:
                attr = var_type.get_attribute(node.identifier)
                node.comp_type = attr.type
            except OrbisimSemanticError as err:
                self.log.append(err.error_info)

    @visitor.when(ClassMakeNode)
    def check(self, node: ClassMakeNode, scope: 'Scope'):
        class_type: 'OrbsimType' = self.context.get_type(node.classname)
        attrs = class_type.attributes
        for  p in node.params:
            self.check(p, scope)
        
        for index, att in enumerate(attrs.values()):
            if att.type != node.params[index].comp_type:
                self.log.append(f'No le puedes asignar a un atributo de tipo {att.type.name} una expresión de tipo {node.params[index].comp_type}')
            
        node.comp_type = class_type


    @visitor.when(MethodCallNode)
    def check(self, node: MethodCallNode, scope: 'Scope'):
        if not scope.check_var(node.instance_name):
            self.log.append(f'No existe la variable {node.instance_name}')
        else:
            var_info = scope.get_variable(node.instance_name)
            
            try:
                t_method:'Method' = var_info.type.get_method(node.identifier, len(node.args))
                for arg_index, arg_type in enumerate(t_method.type_args):
                    self.check(node.args[arg_index], scope)
                    arg_comp_type = node.args[arg_index].comp_type
                    if arg_comp_type != arg_type and arg_type != AnyType():
                        self.log.append(f'Se esperaba una expresión de tipo {arg_type.name} para el argumento {t_method.args[arg_index]} del método {node.identifier} de la clase {node.instance_name}')
                node.comp_type = t_method.return_type
            except OrbisimSemanticError as err:
                self.log.append(err.error_info)



    @visitor.when(StringNode)
    def check(self, node: StringNode, scope: 'Scope'):
        node.comp_type = StringType()
    
    @visitor.when(IntegerNode)
    def check(self, node: IntegerNode, scope: 'Scope'):
        node.comp_type = IntType()
    
    @visitor.when(FloatNode)
    def check(self, node: FloatNode, scope: 'Scope'):
        node.comp_type = FloatType()
    
    @visitor.when(BooleanNode)
    def check(self, node: BooleanNode, scope: 'Scope'):
        node.comp_type = BoolType()
    
    @visitor.when(ListCreationNode)
    def check(self, node: ListCreationNode, scope: 'Scope'):
        list_type = []
        for expr in node.elems:
            self.check(expr, scope)
            if list_type:
                if list_type[::-1][0] != expr.comp_type:
                    self.log.append(f'Todos los elementos de una lista deben ser del mismo tipo')
                    return
            else:
                list_type.append(expr.comp_type)
        
        node.comp_type = ListType()
        if list_type:
            node.comp_type.elems_type = list_type[0]