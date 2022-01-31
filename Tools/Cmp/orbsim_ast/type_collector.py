
from dataclasses import dataclass
from typing import List
from Context import Context
import visitor as visitor
from program_node import ProgramNode
from class_declr import ClassDeclr
from logger import  Logger

@dataclass
class TypeCollector:
    context: Context = Context()
    logger: List[str] = []
    

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context: Context =  Context()
        self.context.create_type('String', self.logger)
        
        self.context.create_type('Bool', self.logger)
        self.context.create_type('Integer', self.logger)
        self.context.create_type('Float', self.logger)

        for st in node.statements:
            self.visit(st)
    
    @visitor.when(ClassDeclr)
    def visit(self, node: ClassDeclr):
        self.context.create_type(node.name, self.logger)

        
    

        

        

        
        
        

        

