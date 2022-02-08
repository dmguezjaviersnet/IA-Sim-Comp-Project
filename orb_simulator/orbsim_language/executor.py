from orbsim_language.orbsim_ast.body_node import BodyNode
import orbsim_language.visitor as visitor
from orbsim_language.orbsim_ast.program_node import ProgramNode
from orbsim_language.orbsim_ast.variable_declr_node import VariableDeclrNode
from orbsim_language.context import Scope
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
from orbsim_language.context import Context, Scope, ExScope
from orbsim_language.orbsim_ast.variable_node import VariableNode
from orbsim_language.orbsim_ast.assign_node import AssingNode
from orbsim_language.orbsim_ast.func_declr_node import FuncDeclrNode
from orbsim_language.orbsim_ast.fun_call_node import FunCallNode
from orbsim_language.built_in_funcs import*
from orbsim_language.orbsim_ast.attribute_declr_node import AttributeDeclrNode

class Executor:

    
    def __init__(self, context: 'Context'):
        self.context: 'Context' = context
        self.builtin_funcs = {
            'concat':concat
        }
        # self.scope: 'ExScope' = ExScope()

    @visitor.on('node')
    def execute(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def execute(self, node: 'ProgramNode', scope: 'ExScope'):
        for st in node.statements:
            self.execute(st, scope)
    
    @visitor.when(VariableDeclrNode)
    def execute(self, node:'VariableDeclrNode',  scope: 'ExScope'):
        # def_values = {'string': '', 'int': 0, 'bool': False}
        ex_expr = self.execute(node.expr, scope)
        var_type =  self.context.get_type(node.type)
        scope.define_var(node.identifier, var_type, ex_expr)
        # if not node.expr and node.type in def_values:
        #     instance  = def_values[node.type]
        # else:
        #     instance = self.visit(node.expr, scope)
        # return instance
    @visitor.when(FuncDeclrNode)
    def execute(self, node: FuncDeclrNode, scope: 'ExScope'):
        # ret_type = self.context.get_type(node.return_type)
        # arg_types = [self.context.get_type(t) for t in node.arg_types]
        func = self.context.get_func(node.identifier, len(node.args))
        func.body = node.body
        # self.context.define_fun(node.identifier, ret_type, node.args, arg_types, node.body)
    
    
    @visitor.when(FunCallNode)
    def execute(self, node: FunCallNode, scope: 'ExScope'):
        func = self.context.get_func(node.identifier, len(node.args))
        new_scope = ExScope()
        for i in range(len(node.args)):
            val = self.execute(node.args[i], scope)
            new_scope.define_var(func.args[i],  func.arg_types[i], val)
        return self.execute(func.body, new_scope)
        

    @visitor.when(LoopNode)
    def execute(self, node: 'LoopNode', scope: 'ExScope'):
        while self.execute(node.condition, scope):
            new_scope = scope.create_child_scope()
            self.execute(node.body, new_scope)
    
    @visitor.when(ConditionalNode)
    def execute(self, node: 'ConditionalNode', scope: 'ExScope'):
        if self.execute(node.if_expr, scope):
            return self.execute(node.then_expr, scope.create_child_scope())
        return self.execute(node.else_expr, scope.create_child_scope())
    
    @visitor.when(BodyNode)
    def execute(self, node: 'BodyNode', scope: 'ExScope'):
        instance = None
        for st in node.statements:
            instance = self.execute(st, scope)
        return instance
            
    @visitor.when(IntegerNode)
    def execute(self, node: 'IntegerNode', scope: 'ExScope'):
        return int(node.val)
    
    @visitor.when(BooleanNode)
    def execute(self, node: 'BooleanNode', scope: 'ExScope'):
        if node.val == 'true':
            return True
        return False
    
    @visitor.when(FloatNode)
    def execute(self, node: 'FloatNode', scope: 'ExScope'):
        return float(node.val)
    
    @visitor.when(StringNode)
    def execute(self, node: 'StringNode', scope: 'ExScope'):
        return str(node.val)

    @visitor.when(PrintNode)
    def execute(self, node: 'PrintNode', scope: 'ExScope'):
        eval_expr = self.execute(node.expr, scope)
        print(eval_expr) # temporal hasta que pongamos una consolita en la UI
    
    @visitor.when(NotNode)
    def execute(self, node: 'NotNode', scope: 'ExScope'):
       eval_expr = self.execute(node.expr, scope)
       return not eval_expr
    
    @visitor.when(PlusNode)
    def execute(self, node: 'PlusNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left + eval_right
    
    @visitor.when(MinusNode)
    def execute(self, node: 'MinusNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left - eval_right
    
    @visitor.when(DivNode)
    def execute(self, node: 'DivNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left / eval_right
    
    @visitor.when(ProductNode)
    def execute(self, node: 'ProductNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left * eval_right
    
    @visitor.when(ModNode)
    def execute(self, node: 'ModNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left % eval_right
    
    @visitor.when(EqualNode)
    def execute(self, node: 'EqualNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left == eval_right

    @visitor.when(NotEqualNode)
    def execute(self, node: 'NotEqualNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left != eval_right

    @visitor.when(GreaterThanNode)
    def execute(self, node: 'GreaterThanNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left > eval_right
    
    @visitor.when(GreaterEqualNode)
    def execute(self, node: 'GreaterEqualNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left >= eval_right
    
    @visitor.when(LessThanNode)
    def execute(self, node: 'LessThanNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left < eval_right
    
    @visitor.when(LessEqualNode)
    def execute(self, node: 'LessEqualNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left <= eval_right
    
    @visitor.when(AndNode)
    def execute(self, node: 'AndNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left and eval_right
    
    @visitor.when(OrNode)
    def execute(self, node: 'OrNode', scope: 'ExScope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left or eval_right

    @visitor.when(RetNode)
    def execute(self, node: RetNode, scope: 'ExScope'):
        eval_expr = self.execute(node.expr, scope)
        return eval_expr

    @visitor.when(VariableNode)
    def execute(self, node: VariableNode, scope: 'ExScope'):
        val = scope.get_variable_val(node.identifier)
        return val
    
    @visitor.when(AssingNode)
    def execute(self, node: AssingNode, scope: 'ExScope'):
        new_value = self.execute(node.expr, scope)
        scope.assing_new_variable_val(node.var_id, new_value)
