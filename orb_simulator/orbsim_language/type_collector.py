from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast import ProgramNode, ClassDeclrNode
from orbsim_language.context import Context
from orbsim_language.logger import  Logger
from orbsim_language import visitor as visitor
from errors import OrbisimSemanticError
class TypeCollector:
    context: Context = Context()
    log: List[str] = []  # donde se van guardando los errores
    

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context: Context =  Context()
        self.context.create_type('String')
        
        self.context.create_type('Bool')
        self.context.create_type('Integer')
        self.context.create_type('Float')

        for st in node.statements:
            self.visit(st)
    
    @visitor.when(ClassDeclrNode)
    def visit(self, node: ClassDeclrNode):
        try:
            self.context.create_type(node.name)
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)

        
    

        

        

        
        
        

        

