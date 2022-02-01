from dataclasses import dataclass
from typing import Dict, List, Type
from orbsim_language.orbsim_type import OrbsimType

class OrbisimSemanticError(Exception):
    @property 
    def error(self):
        return self.args[0]
        
@dataclass
class VarInfo:
    name: str

    def __eq__(self, other: 'VarInfo') -> bool:
        return self.name == other.name


@dataclass
class FuncInfo:
    name: str
    args: List[str]

    def __eq__(self, other: 'FuncInfo') -> bool:
        return self.name == other.name and self.args == other.args


class Scope:
    '''
        Para la correcta definición de variables y 
        métodos(el contexto de las variables y métodos)
    '''

    def __init__(self, parent: 'Scope' = None):
        self.parent: 'Scope' = parent
        self.local_variables = {}
        self.local_functions = {}
    
    def check_var(self, var: str) -> bool:
        if var  in self.local_variables:
            return True
        if self.parent != None:
            return self.parent.check_var(var)
        return False
    

    def check_fun(self, fun: str, args: List[str]):
        if (fun, args) in self.local_functions:
            return True
        
        if self.parent != None:
            return self.parent.check_fun(fun, args)
        
        return False
    
    def define_var(self, var: str) -> bool:
        if not self.check_var(var):
            self.local_variables[var] = VarInfo(var)
            return True
        
        return False

    def define_fun(self, fun: str, args: List[str]) -> bool:
        if not self.check_fun(fun, args):
            self.local_functionsp[(fun, args)] = FuncInfo(fun, args)
            return True
        return False
    
    def create_child_scope(self):
        child_scope = Scope(self)
        return child_scope

class Context:
    '''
        Para la correcta definición de los tipos (contexto de los tipos)
    '''

    def __init__(self, parent: 'Context' = None):
        self.parent: 'Context' = parent   
        self.types: Dict[str, Type] = {}
        

    def create_child_context(self):
        child_context = Context(self)
        return child_context
    
    def get_type(self, name: str):
        if name in self.types:
            return self.types[name]
        else:
            return None

    def type_of(symbol: str):
        pass
    
    def define_symbol(symbol: str, type):
        pass
        
    def create_type(self, name: str, logger: List[str]):
        if name in self.types:
            logger.append(f'El tipo ({name}) ya está definido en el contexto')
            return None
        else:
            new_type = OrbsimType(name)
            self.types[name] = new_type
            return new_type
