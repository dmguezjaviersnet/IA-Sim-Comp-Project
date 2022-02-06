from dataclasses import dataclass
from typing import Dict, List

from numpy import imag
from orbsim_language.orbsim_ast import ExpressionNode
from orbsim_language.orbsim_ast import StatementNode
from errors import OrbisimSemanticError
@dataclass
class Attribute:
    name: str
    type: 'OrbsimType'
    expr: 'ExpressionNode'


@dataclass
class Method:
    name: str
    return_type: 'OrbsimType'
    arguments: List['Attribute']
    body: List['StatementNode']
    

class OrbsimType:

    def __init__(self, name: str):
        self.name = name
        self.attributes:  Dict[str, 'Attribute'] = {}
        self.methods: Dict[str, 'Method'] = {}
    

    def get_attribute(self, name: str) -> 'Attribute':
        return self.attributes[name]
    
    def get_method(self, name: str):
        return self.methods[name]
    
    def define_attribute(self, name: str, type: 'OrbsimType') -> bool:
        if name in self.attributes:
            raise OrbisimSemanticError(f'Ya existe un atributo definido con en {type.name} con este nombre')
        self.attributes[name] = Attribute(name, type)
        return True
    
    def define_method(self, name: str, return_type:'OrbsimType', args: List[str], arg_types: List['OrbsimType']) -> bool:
        if name in self.methods:
            return False
        arguments = [Attribute(arg, arg_type) for arg, arg_type in zip(args, arg_types)]
        self.methods[name] = Method(name, return_type, arguments)
        return True

class VoidType(OrbsimType):
    def __init__(self):
        OrbsimType.__init__(self, 'Void')
    
    def __eq__(self, other):
        return isinstance(other, VoidType)


def NullType(OrbsimType):
    def __init__(self):
        OrbsimType.__init__(self, 'Null')
    def __eq__(self, other):
        return isinstance(other, NullType)


