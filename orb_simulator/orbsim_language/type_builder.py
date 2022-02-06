from typing import List
from orbsim_language import visitor
from orbsim_language.context import Context
from orbsim_language.orbsim_type import OrbsimType
from orbsim_language.orbsim_ast import MethodDeclrNode, ProgramNode
from orbsim_language.orbsim_ast import ClassDeclrNode, AttributeDef
from errors import OrbisimSemanticError
class TypeBuilder:
    def __init__(self,  context: 'Context', log: List[str] = []):
        self.context = context
        self.log: List[str] = log
        self.current_type: 'OrbsimType' =  None

    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node: 'ProgramNode'):
        for statement in node.statements:
            self.visit(statement)
    
    @visitor.when(ClassDeclrNode)
    def visit(self, node: ClassDeclrNode):
        self.current_type = self.context.get_type(node.name)

        for attribute in node.attributes:
            self.visit(attribute)
        
        for method in node.methods:
            self.visit(method)

    @visitor.when(AttributeDef)
    def visit(self, node: AttributeDef):
        try:
            attr_type = self.context.get_type(node.type)
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)
        try:
            self.current_type.define_attribute(node.name, attr_type)
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)

    @visitor.when(MethodDeclrNode)
    def visit(self, node: MethodDeclrNode):
        try:
            return_type = self.context.get_type(node.return_type)
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)
        
        arg_types = [self.context.get_type(t) for t in node.arg_types]
        self.current_type.define_method(node.name, return_type, node.arg_names, arg_types)
        





        

