from dataclasses import dataclass
from typing import Any, List
from orbsim_language.orbsim_ast import ProgramNode, ClassDeclrNode
from orbsim_language.context import Context
from orbsim_language.orbsim_type import AnyType, ListType, OrbsimType, VoidType, StringType, BoolType, IntType, FloatType, SimType
from orbsim_language.logger import  Logger
from orbsim_language import visitor as visitor

from errors import OrbisimSemanticError
class TypeCollector:

    def __init__(self, context: Context = Context(), log: List[str] = []):
        self.context = context
        self.log: List[str] = []  # donde se van guardando los errores
   
    

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context: Context =  Context()
        self.context.define_fun('randint', IntType(), ['init_range', 'fin_range'], [IntType(), IntType()])
        self.context.define_fun('randfloat', FloatType(), ['init_range', 'fin_range'], [IntType(), IntType()])
        string_type =  StringType()
        self.context.types['String']  = string_type
        string_type.define_method('concat', string_type, ['s1'], [string_type])
        string_type.define_method('len', IntType(), [], [])
        bool_type = BoolType()
        self.context.types['Bool']  =  bool_type
        int_type =  IntType()
        self.context.types['Int'] =  int_type
        float_type = FloatType()
        self.context.types['Float'] =  float_type
        list_type = ListType()
        self.context.types['List'] = list_type
        list_type.define_method('len', IntType(), [], [])
        list_type.define_method('add', ListType(), ['elem'], [AnyType()])
        list_type.define_method('remove', ListType(), ['elem'], [AnyType()])
        self.context.types['Void'] = VoidType()
        self.context.types['Any'] = AnyType()
        
        
        for st in node.statements:
            self.visit(st)
    
    @visitor.when(ClassDeclrNode)
    def visit(self, node: ClassDeclrNode):
        try:
            self.context.create_type(node.name)
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)

        
    

        

        

        
        
        

        

