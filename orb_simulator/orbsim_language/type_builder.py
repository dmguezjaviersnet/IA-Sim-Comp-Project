from orbsim_language import visitor
from orbsim_language.context import Context
from orbsim_language.orbsim_type import OrbsimType
from orbsim_language.orbsim_ast import MethodDef, ProgramNode
from orbsim_language.orbsim_ast import ClassDeclr, AttributeDef

class TypeBuilder:
    def __init__(self,  context: 'Context', logger):
        self.context = context
        self.logger = logger
        self.current_type: 'OrbsimType' =  None

    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: 'ProgramNode'):
        for statement in node.statements:
            self.visit(statement)
    
    @visitor.when(ClassDeclr)
    def visit(self, node: ClassDeclr):
        self.current_type = self.context.get_type(node.name)

        for attribute in node.attributes:
            self.visit(attribute)
        
        for method in node.methods:
            self.visit(method)

    @visitor.when(AttributeDef)
    def visit(self, node: AttributeDef):
        attr_type = self.context.get_type(node.type)
        self.current_type.define_attribute(node.name, attr_type)
    
    @visitor.when(MethodDef)
    def visit(self, node: 'MethodDef'):
        return_type = self.context.get_type(node.return_type)
        arg_types = [self.context.get_type(t) for t in node.arg_types]
        self.current_type.define_method(node.name, return_type, node.arg_names, arg_types)
        





        

