from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Attribute:
    name: str
    type: 'OrbsimType'


@dataclass
class Method:
    name: str
    return_type: 'OrbsimType'
    arguments: List['Attribute']
    

class OrbsimType:
    name: str
    attributes:  Dict[str, 'Attribute'] = {}
    methods: Dict[str, 'Method'] = {}

    def get_attribute(self, name: str) -> 'Attribute':
        return self.attributes[name]
    
    def get_method(self, name: str):
        return self.methods[name]
    
    def define_attribute(self, name: str, type: 'OrbsimType') -> bool:
        if name in self.attributes:
            return False
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


