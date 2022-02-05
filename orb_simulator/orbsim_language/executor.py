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

class Executor:

    def __init__(self):
        pass

    @visitor.on('node')
    def execute(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def execute(self, node: 'ProgramNode', scope: 'Scope'):
        for st in node.statements:
            self.execute(st, scope)
    
    @visitor.when(VariableDeclrNode)
    def execute(self, node:'VariableDeclrNode',  scope: 'Scope'):
        def_values = {'string': '', 'int': 0, 'bool': False}
        if not node.expr and node.type in def_values:
            instance  = def_values[node.type]
        else:
            instance = self.visit(node.expr, scope)
        return instance
    
    @visitor.when(LoopNode)
    def execute(self, node: 'LoopNode', scope: 'Scope'):
        while self.visit(node.condition, scope):
            self.visit(node.body, scope.create_child_scope())
    
    @visitor.when(ConditionalNode)
    def execute(self, node: 'ConditionalNode', scope: 'Scope'):
        if self.visit(node.if_expr, scope):
            return self.visit(node.then_expr, scope.create_child_scope())
        return self.visit(node.else_expr, scope.create_child_scope())
    
    @visitor.when(IntegerNode)
    def execute(self, node: 'IntegerNode', scope: 'Scope'):
        return int(node.val)
    
    @visitor.when(BooleanNode)
    def execute(self, node: 'BooleanNode', scope: 'Scope'):
        if node.val == 'true':
            return True
        return False
    
    @visitor.when(FloatNode)
    def execute(self, node: 'FloatNode', scope: 'Scope'):
        return float(node.val)
    
    @visitor.when(StringNode)
    def execute(self, node: 'StringNode', scope: 'Scope'):
        return str(node.val)

    @visitor.when(PrintNode)
    def execute(self, node: 'PrintNode', scope: 'Scope'):
        eval_expr = self.execute(node.expr)
        print(eval_expr) # temporal hasta que pongamos una consolita en la UI
    
    @visitor.when(NotNode)
    def execute(self, node: 'NotNode', scope: 'Scope'):
       eval_expr = self.visit(node.expr)
       return not eval_expr
    
    @visitor.when(PlusNode)
    def execute(self, node: 'PlusNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left + eval_right
    
    @visitor.when(MinusNode)
    def execute(self, node: 'MinusNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left - eval_right
    
    @visitor.when(DivNode)
    def execute(self, node: 'DivNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left / eval_right
    
    @visitor.when(ProductNode)
    def execute(self, node: 'ProductNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left * eval_right
    
    @visitor.when(ModNode)
    def execute(self, node: 'ModNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left % eval_right
    
    @visitor.when(EqualNode)
    def execute(self, node: 'EqualNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left == eval_right

    @visitor.when(NotEqualNode)
    def execute(self, node: 'NotEqualNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left != eval_right

    @visitor.when(GreaterThanNode)
    def execute(self, node: 'GreaterThanNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left > eval_right
    
    @visitor.when(GreaterEqualNode)
    def execute(self, node: 'GreaterEqualNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left >= eval_right
    
    @visitor.when(LessThanNode)
    def execute(self, node: 'LessThanNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left < eval_right
    
    @visitor.when(LessEqualNode)
    def execute(self, node: 'LessEqualNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left <= eval_right
    
    @visitor.when(AndNode)
    def execute(self, node: 'AndNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left and eval_right
    
    @visitor.when(OrNode)
    def execute(self, node: 'OrNode', scope: 'Scope'):
        eval_left = self.execute(node.left, scope)
        eval_right = self.execute(node.right, scope)
        return eval_left or eval_right

    @visitor.when(RetNode)
    def execute(self, node: RetNode, scope: 'Scope'):
        eval_expr = self.execute(node.expr, scope)
        return eval_expr

    