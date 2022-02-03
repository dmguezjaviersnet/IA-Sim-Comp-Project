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
    