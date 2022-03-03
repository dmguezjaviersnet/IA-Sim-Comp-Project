from dataclasses import dataclass
from typing import Any, List


from orbsim_language.orbsim_ast import ProgramNode, ClassDeclrNode
from orbsim_language.context import Context
from orbsim_language.orbsim_type import AgentType, AnyType, ListType, OrbsimType, VoidType, StringType, BoolType, IntType, FloatType, OrbitType, SatelliteType, SpaceDebrisType, TupleType
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
        self.context.define_fun('number_orbits', IntType(), [], [])
        self.context.define_fun('number_space_debris', IntType(), [], [])
        self.context.define_fun('number_satellites', IntType(), [], [])
        self.context.define_fun('number_objects', IntType(), [], [])
        self.context.define_fun('custom_space_debris', SpaceDebrisType(), ['size', 'color'], [TupleType(), TupleType()])
        self.context.define_fun('custom_launchpad', VoidType(), ['T', 'lambda'], [IntType(), FloatType()])
        self.context.define_fun('custom_create_space_debris_event', VoidType(), ['T', 'lambda'], [IntType(), FloatType()])
        self.context.define_fun('custom_create_agent', AgentType(), ['lifetime', 'capacity', 'fuel', 'perception_range', 'vel'],[IntType(), IntType(), IntType(), IntType(), IntType()])
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
        tuple_type =  TupleType()
        self.context.types['Tuple'] = tuple_type
        self.context.types['Void'] = VoidType()
        self.context.types['Any'] = AnyType()
        orbit_type = OrbitType() 
        self.context.types['Orbit'] =  orbit_type
        orbit_type.define_method('add_to_simulation', VoidType(), [], [])
        satellite_type =  SatelliteType()
        self.context.types['Satellite'] = satellite_type
        satellite_type.define_method('add_to_simulation', VoidType(), [], [])
        space_debris_type = SpaceDebrisType()
        self.context.types['SpaceDebris'] = space_debris_type
        space_debris_type.define_method('add_to_simulation', VoidType(), [], [])
        space_debris_type.define_method('move_to_orbit', VoidType(), ['orbit'], [OrbitType()])
        agent_type = AgentType()
        self.context.types['Agent'] = agent_type
        agent_type.define_method('add_to_simulation', VoidType(), [], [])
        
        
        for st in node.statements:
            self.visit(st)
    
    @visitor.when(ClassDeclrNode)
    def visit(self, node: ClassDeclrNode):
        try:
            self.context.create_type(node.name)
        except OrbisimSemanticError as err:
            self.log.append(err.error_info)

        
    

        

        

        
        
        

        

