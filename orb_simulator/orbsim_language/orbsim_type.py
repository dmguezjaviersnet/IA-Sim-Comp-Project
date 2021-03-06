from dataclasses import dataclass
from typing import Any, Dict, List

from numpy import imag
from orbsim_language.orbsim_ast import ExpressionNode
from orbsim_language.orbsim_ast import StatementNode
from orbsim_language.orbsim_ast import BodyNode
from errors import OrbisimSemanticError
@dataclass
class Attribute:
    name: str
    type: 'OrbsimType'
    expr: 'ExpressionNode' =  None
    val: Any = None

@dataclass
class Method:
    name: str
    return_type: 'OrbsimType'
    args: str
    type_args: List['OrbsimType']
    body: 'BodyNode' = None
    

class OrbsimType:

    def __init__(self, name: str):
        self.name = name
        self.attributes:  Dict[str, 'Attribute'] = {}
        self.methods: Dict[(str, int), 'Method'] = {}
    

    def get_attribute(self, name: str) -> 'Attribute':
        try:
            return self.attributes[name]
        except KeyError:
            raise OrbisimSemanticError(f'El tipo {self.name} no tiene definido ningún atributo {name}')
        
    def get_method(self, name: str, args: int) -> 'Method':
        try:
            return self.methods[(name, args)]
        except KeyError:
            raise OrbisimSemanticError(f'El tipo {self.name} not tiene un método definido con nombre {name} y {args} argumentos')

    
    def define_attribute(self, name: str, type: 'OrbsimType') -> bool:
        if name in self.attributes:
            raise OrbisimSemanticError(f'Ya existe un atributo definido con en {type.name} con este nombre')
        self.attributes[name] = Attribute(name, type)
        return True
    
    def define_method(self, name: str, return_type:'OrbsimType', args: List[str], arg_types: List['OrbsimType'], body = None) -> bool:
        if (name, len(args)) in self.methods:
            raise OrbisimSemanticError(f'Ya existe un método definido con nombre{name} y cantidad de parámetros{len(args)}')
        
        self.methods[(name, len(args))] = Method(name, return_type, args, arg_types, body)
        return True

    def __eq__(self, other: 'OrbsimType'):
        return self.name == other.name
    
    def __ne__(self, other: 'OrbsimType'):
        return self.name != other.name
class VoidType(OrbsimType):
    def __init__(self):
        OrbsimType.__init__(self, 'Void')
    

class IntType(OrbsimType):
    def __init__(self):
        OrbsimType.__init__(self, 'Int')
    
class StringType(OrbsimType):
    def __init__(self):
        OrbsimType.__init__(self, 'String')

class FloatType(OrbsimType):
    def __init__(self):
        OrbsimType.__init__(self, 'Float')
    
class BoolType(OrbsimType):
    def __init__(self):
        OrbsimType.__init__(self, 'Bool')

class OrbitType(OrbsimType):
    def __init__(self):
        super().__init__('Orbit')

class SatelliteType(OrbsimType):
    def __init__(self):
        super().__init__('Satellite')

class SpaceDebrisType(OrbsimType):
    def __init__(self):
        super().__init__('SpaceDebris')
class AgentType(OrbsimType):
    def __init__(self):
        super().__init__('Agent')

class ListType(OrbsimType):
    def __init__(self):
        super().__init__('List')
        self.elems_type: OrbsimType = None

class TupleType(OrbsimType):
    def __init__(self):
        super().__init__('Tuple')
        self.elems_type: OrbsimType = None
class AnyType(OrbsimType):
    def __init__(self):
        super().__init__('Any')

class SimType(OrbsimType):
    def __init__(self):
        super().__init__('Sim')

class NullType(OrbsimType):
    def __init__(self):
        OrbsimType.__init__(self, 'Null')
