import random

from orbsim_language.orbsim_ast.body_node import BodyNode
import orbsim_language.visitor as visitor
from orbsim_language.orbsim_ast.program_node import ProgramNode
from orbsim_language.orbsim_ast.variable_declr_node import VariableDeclrNode
from orbsim_language.context import Scope, VariableInfo
from orbsim_language.orbsim_ast.loop_node import LoopNode
from orbsim_language.orbsim_ast.conditional_node import ConditionalNode
from orbsim_language.orbsim_ast.boolean_node import BooleanNode
from orbsim_language.orbsim_ast.integer_node import IntegerNode
from orbsim_language.orbsim_ast.float_node import FloatNode
from orbsim_language.orbsim_ast.string_node import StringNode
from orbsim_language.orbsim_ast.print_node import PrintNode
from orbsim_language.orbsim_ast.not_node import NotNode
from orbsim_language.orbsim_ast.plus_node import PlusNode
from orbsim_language.orbsim_ast.minus_node import MinusNode
from orbsim_language.orbsim_ast.div_node import DivNode
from orbsim_language.orbsim_ast.mod_node import ModNode
from orbsim_language.orbsim_ast.product_node import ProductNode
from orbsim_language.orbsim_ast.equal_node import EqualNode
from orbsim_language.orbsim_ast.not_equal_node import NotEqualNode
from orbsim_language.orbsim_ast.greater_than_node import GreaterThanNode
from orbsim_language.orbsim_ast.greater_equal_node import GreaterEqualNode
from orbsim_language.orbsim_ast.less_than_node import LessThanNode
from orbsim_language.orbsim_ast.less_equal_node import LessEqualNode
from orbsim_language.orbsim_ast.and_node import AndNode
from orbsim_language.orbsim_ast.or_node import OrNode
from orbsim_language.orbsim_ast.ret_node import RetNode
from orbsim_language.context import Context, Scope
from orbsim_language.orbsim_ast.variable_node import VariableNode
from orbsim_language.orbsim_ast.assign_node import AssingNode
from orbsim_language.orbsim_ast.func_declr_node import FuncDeclrNode
from orbsim_language.orbsim_ast.fun_call_node import FunCallNode
from orbsim_language.orbsim_ast.attribute_declr_node import AttributeDeclrNode
from orbsim_language.orbsim_ast.bitwise_and_node import BitwiseAndNode
from orbsim_language.orbsim_ast.bitwise_or_node import BitwiseOrNode
from orbsim_language.orbsim_ast.bitwise_xor_node import BitwiseXorNode
from orbsim_language.orbsim_ast.bitwise_shift_left_node import BitwiseShiftLeftNode
from orbsim_language.orbsim_ast.bitwise_shift_right_node import BitwiseShiftRightNode
from orbsim_language.orbsim_ast.attribute_call_node import AttributeCallNode
from orbsim_language.orbsim_ast.class_make_node import ClassMakeNode
from orbsim_language.instance import Instance
from orbsim_language.orbsim_type import*
from orbsim_language.orbsim_ast.method_call_node import MethodCallNode
from orbsim_language.orbsim_ast.method_declr_node import MethodDeclrNode
from orbsim_language.orbsim_ast.list_creation_node import ListCreationNode
from orbsim_language.orbsim_ast.break_node import BreakNode
from orbsim_language.orbsim_ast.continue_node import ContinueNode
from orbsim_language.builtins import *
from orbsim_language.orbsim_ast.neg_number_node import NegNumberNode
from orbsim_language.orbsim_ast.start_sim_node import StartSimNode
from orbsim_language.orbsim_ast.stop_sim_node import StopSimNode
from orbsim_language.orbsim_ast.pause_sim_node import PauseSimNode
from orbsim_language.orbsim_ast.drawquadtree_node import DrawquadtreeNode
from orbsim_language.orbsim_ast.animate_earth_node import AnimateEarthNode
from orbsim_language.orbsim_ast.orbit_node import OrbitNode
from orbsim_language.orbsim_ast.satellite_node import SatelliteNode
from orbsim_language.orbsim_ast.space_debris_node import SpaceDebrisNode
from orbsim_language.orbsim_ast.show_orbits_node import ShowOrbitsNode
from orbsim_language.orbsim_ast.agent import AgentNode
from orbsim_language.orbsim_ast.tuple_creation_node import TupleCreationNode
from simulation.generate_objects import *
from orbsim_pygame import PygameHandler
import orbsim_pygame
import threading
from errors import OrbisimExecutionError
class Executor:

    
    def __init__(self, context: 'Context', handler):
        self.context: 'Context' = context
        self.log: List[str] = []
        self.handler: 'PygameHandler' = handler
        self.break_unchained = False
        # self.scope: 'Scope' = Scope()

    @visitor.on('node')
    def execute(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def execute(self, node: 'ProgramNode', scope: 'Scope'):
        for st in node.statements:
            self.execute(st, scope)
    
    @visitor.when(VariableDeclrNode)
    def execute(self, node:'VariableDeclrNode',  scope: 'Scope'):
        instance_expr = self.execute(node.expr, scope)
        var_type =  self.context.get_type(node.type)
        scope.define_var(node.identifier, var_type)
        scope.get_variable(node.identifier).instance = instance_expr
        

    @visitor.when(FuncDeclrNode)
    def execute(self, node: FuncDeclrNode, scope: 'Scope'):
        
        func = self.context.get_func(node.identifier, len(node.args))
        func.body = node.body
       
    
    
    @visitor.when(FunCallNode)
    def execute(self, node: FunCallNode, scope: 'Scope'):
        func = self.context.get_func(node.identifier, len(node.args))
        new_scope = Scope()
        if (node.identifier) in builtins_functions:
            args = tuple(self.execute(expr, scope) for expr in node.args)
            if for_simulation(node.identifier):
                args =  args + (self.handler,)
            return builtins_functions[(node.identifier)](*args)
        
        for i in range(len(node.args)):
            var_instance = self.execute(node.args[i], scope)
            new_scope.define_var(func.args[i],  func.arg_types[i])
            new_scope.get_variable(func.args[i]).instance =  var_instance
        return self.execute(func.body, new_scope)
    

    @visitor.when(LoopNode)
    def execute(self, node: 'LoopNode', scope: 'Scope'):
        while self.execute(node.condition, scope).value:
            new_scope = scope.create_child_scope()
            instance = self.execute(node.body, new_scope)
            if instance == 'continue':
                continue
            if instance == 'break':
                break
    @visitor.when(ConditionalNode)
    def execute(self, node: 'ConditionalNode', scope: 'Scope'):
        if self.execute(node.if_expr, scope).value:
            return self.execute(node.then_expr, scope.create_child_scope())
        return self.execute(node.else_expr, scope.create_child_scope())
    
    @visitor.when(BodyNode)
    def execute(self, node: 'BodyNode', scope: 'Scope'):
        instance = None
        for st in node.statements:
            if isinstance(st, ContinueNode):
                return 'continue'
            if isinstance(st, BreakNode):
                return 'break'
            instance = self.execute(st, scope)
        return instance
    
    
    @visitor.when(IntegerNode)
    def execute(self, node: 'IntegerNode', scope: 'Scope'):
        return Instance(IntType(),int(node.val))
    

    @visitor.when(BooleanNode)
    def execute(self, node: 'BooleanNode', scope: 'Scope'):
        if node.val == 'true':
            return  Instance(BoolType(), True)
        return Instance(BoolType(), False)
    
    @visitor.when(FloatNode)
    def execute(self, node: 'FloatNode', scope: 'Scope'):
        return Instance(FloatType(), float(node.val))
    
    @visitor.when(StringNode)
    def execute(self, node: 'StringNode', scope: 'Scope'):
        return Instance(StringType(), str(node.val))

    @visitor.when(PrintNode)
    def execute(self, node: 'PrintNode', scope: 'Scope'):
        instance_expr: 'Instance' = self.execute(node.expr, scope)
        print(instance_expr.value) # temporal hasta que pongamos una consolita en la UI
    
    @visitor.when(NotNode)
    def execute(self, node: 'NotNode', scope: 'Scope'):
       instance_expr: 'Instance' = self.execute(node.expr, scope)
       return Instance(BoolType(), not instance_expr.value)
    
    @visitor.when(PlusNode)
    def execute(self, node: 'PlusNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        if instance_right.orbsim_type.name == 'Int':
            plus_type  = IntType()
        else:
            plus_type  = FloatNode()
        return Instance(plus_type, instance_left.value + instance_right.value)
    
    @visitor.when(MinusNode)
    def execute(self, node: 'MinusNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        if instance_right.orbsim_type.name == 'Int':
            minus_type  = IntType()
        else:
            minus_type  = FloatNode()
        return Instance(minus_type, instance_left.value - instance_right.value)
    
    @visitor.when(DivNode)
    def execute(self, node: 'DivNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        try:
            instance_div_val = instance_left / instance_right
            instance_div_type = FloatType()
        except ZeroDivisionError:
            raise OrbisimExecutionError(f'ZeroDivisionError: Division por 0')
        
        if instance_left.orbsim_type.name == 'Int':
            instance_div_val = int(instance_div_val)
            instance_div_type = FloatType()
        
        return Instance(IntType(), instance_div_type)  
            
    
    @visitor.when(ProductNode)
    def execute(self, node: 'ProductNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        
        if instance_right.orbsim_type.name == 'Int':
            prod_type  = IntType()
        else:
            prod_type  = FloatNode()
        
        return Instance(prod_type, instance_left.value * instance_right.value)
    
    @visitor.when(ModNode)
    def execute(self, node: 'ModNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(IntType(), instance_left.value % instance_right.value)
    
    @visitor.when(EqualNode)
    def execute(self, node: 'EqualNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(BoolType(), instance_left.value == instance_right.value)

    @visitor.when(NotEqualNode)
    def execute(self, node: 'NotEqualNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(BoolType(), instance_left.value != instance_right.value)

    @visitor.when(GreaterThanNode)
    def execute(self, node: 'GreaterThanNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(BoolType(), instance_left.value > instance_right.value)
    
    @visitor.when(GreaterEqualNode)
    def execute(self, node: 'GreaterEqualNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(BoolType(), instance_left.value >= instance_right.value)
    
    @visitor.when(LessThanNode)
    def execute(self, node: 'LessThanNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(BoolType(), instance_left.value < instance_right.value)
    
    @visitor.when(LessEqualNode)
    def execute(self, node: 'LessEqualNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(BoolType(), instance_left.value <= instance_right.value)
    
    @visitor.when(AndNode)
    def execute(self, node: 'AndNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(instance_left.value and instance_right.value)
    
    @visitor.when(OrNode)
    def execute(self, node: 'OrNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(BoolType(), instance_left.value or instance_right.value)

    @visitor.when(BitwiseAndNode)
    def execute(self, node: 'BitwiseAndNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(IntType(), instance_left.value & instance_right.value)
    
    @visitor.when(BitwiseOrNode)
    def execute(self, node: 'BitwiseOrNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(IntType(), instance_left.value | instance_right.value)
    
    @visitor.when(BitwiseXorNode)
    def execute(self, node: 'BitwiseXorNode', scope: 'Scope'):
        instance_left = self.execute(node.left, scope)
        instance_right = self.execute(node.right, scope)
        return Instance(IntType(),instance_left ^ instance_right)
    
    @visitor.when(BitwiseShiftRightNode)
    def execute(self, node: 'BitwiseShiftRightNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(IntType(), instance_left.value >> instance_right.value)
    
    @visitor.when(BitwiseShiftLeftNode)
    def execute(self, node: 'BitwiseShiftLeftNode', scope: 'Scope'):
        instance_left: 'Instance' = self.execute(node.left, scope)
        instance_right: 'Instance' = self.execute(node.right, scope)
        return Instance(IntType(), instance_left.value << instance_right.value)
    
    @visitor.when(RetNode)
    def execute(self, node: RetNode, scope: 'Scope'):
        instance_expr = self.execute(node.expr, scope)
        return instance_expr

    @visitor.when(VariableNode)
    def execute(self, node: VariableNode, scope: 'Scope'):
        var_instance= scope.get_variable(node.identifier).instance
        return var_instance
    
    @visitor.when(AssingNode)
    def execute(self, node: AssingNode, scope: 'Scope'):
        var_info : 'VariableInfo' = scope.get_variable(node.var_id)
        new_instance_value = self.execute(node.expr, scope)
        var_info.instance = new_instance_value
    
        
    @visitor.when(AttributeCallNode)
    def execute(self, node: AttributeCallNode, scope: 'Scope'):
        class_instance: 'Instance' =  scope.get_variable(node.instance_name).instance
        
        return class_instance.get_attr_instance(node.identifier)
    
    @visitor.when(ClassMakeNode)
    def execute(self, node: ClassMakeNode, scope: 'Scope'):
        class_type: 'OrbsimType' = self.context.get_type(node.classname)
        
        class_instance = Instance(class_type)
        for attr_index, attr in enumerate(class_type.attributes):
            attr_instance = self.execute(node.params[attr_index], scope)
            class_instance.set_attr_instance(attr, attr_instance)
        return class_instance

    @visitor.when(MethodCallNode)
    def execute(self, node: MethodCallNode, scope: 'Scope'):
        var: VariableInfo = scope.get_variable(node.instance_name)
        var_instance = var.instance

        new_scope = Scope()
        if (var.type.name, node.identifier) in builtins_methods:
            args = (var.instance ,) + tuple(self.execute(expr, scope) for expr in node.args)
            if for_simulation(node.identifier):
                args = args + (self.handler,)
            return builtins_methods[(var.type.name, node.identifier)](*args)
        
        method: 'Method' = var_instance.get_method(node.identifier, len(node.args))
        new_scope.define_var('this', var_instance.orbsim_type)
        new_scope.get_variable('this').instance = var_instance
        for arg, arg_type, arg_expr in  zip(method.args, method.type_args, node.args):
            new_scope.define_var(arg, arg_type)
            new_var = new_scope.get_variable(arg)
            new_var.instance = self.execute(arg_expr, scope)

        return self.execute(method.body, new_scope)
    
    @visitor.when(ListCreationNode)
    def execute(self, node: ListCreationNode, scope: 'Scope'):
        list_val = []
        for elem in node.elems:
            elem_instance = self.execute(elem, scope)
            list_val.append(elem_instance.value)
        
        return Instance(ListType(), list_val) 
    
    @visitor.when(TupleCreationNode)
    def execute(self, node: TupleCreationNode, scope: 'Scope'):
        tuple_val = ()
        for elem in node.elems:
            elem_instance = self.execute(elem, scope)
            tuple_val += (elem_instance.value,)
        
        return Instance(TupleType(), tuple_val) 

    @visitor.when(NegNumberNode)
    def execute(self, node: NegNumberNode, scope: 'Scope'):
        
        expr_instance = self.execute(node.expr, scope)
        return Instance(IntType(), -expr_instance.value) 
    
    @visitor.when(StartSimNode)
    def execute(self, node: StartSimNode, scope: 'Scope'):
        
        # self.handler.start()
        # self.handler.generate_orbits(random.randint(1,2))
        # self.handler.generate_objects_in_orbits(random.randint(1,1))
        # self.handler.generate_random_collector()
        self.handler.start_pygame()
        
        # t1 = threading.Thread(target=orbsim_pygame.start_simulation, args=())
        # t1.start()
        # t1.join()
    
    @visitor.when(StopSimNode)
    def execute(self, node: 'StopSimNode', scope: 'Scope'):


        self.handler.stop_pygame()
    
    @visitor.when(PauseSimNode)
    def execute(self, node: 'PauseSimNode', scope: 'Scope'):
        self.handler.pause_pygame()
    
    @visitor.when(DrawquadtreeNode)
    def execute(self, node: 'DrawquadtreeNode', scope: 'Scope'):
        self.handler.draw_quadtree()
    
    @visitor.when(AnimateEarthNode)
    def execute(self, node: 'AnimateEarthNode', scope: 'Scope'):
        self.handler.earth_animate()
    
    @visitor.when(OrbitNode)
    def execute(self, node: 'OrbitNode', scope: 'Scope'):
        orbit  = generate_new_random_orbit(self.handler.screen_center)
        return Instance(OrbitType(), orbit)

    @visitor.when(SatelliteNode)
    def execute(self, node: 'SatelliteNode', scope: 'Scope'):
        if not self.handler.orbits:
            self.log.append(f'No existe ninguna ??rbita para ubicar el sat??lite')
        else:
            satellite = generate_new_random_satellite(self.handler.orbits)
            return Instance(SatelliteType(), satellite)

    @visitor.when(SpaceDebrisNode)
    def execute(self, node: 'SpaceDebrisNode', scope: 'Scope'):
        if not self.handler.orbits:
            self.log.append(f'No existe ninguna ??rbita para ubicar el sat??lite')
        else:
            space_debris = generate_new_random_space_debris(self.handler.orbits)
            return Instance(SpaceDebrisType(), space_debris)
    
    @visitor.when(AgentNode)
    def execute(self, node: 'AgentNode', scope: 'Scope'):
        agent =  self.handler.create_random_space_debris_collector()
        return Instance(AgentType(), agent)


    @visitor.when(ShowOrbitsNode)
    def execute(self, node: 'ShowOrbitsNode', scope: 'Scope'):
        self.handler.show_orbits = not self.handler.show_orbits
    