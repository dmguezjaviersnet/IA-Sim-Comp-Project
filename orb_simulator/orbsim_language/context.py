from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Type


# from orbsim_language.orbsim_type import OrbsimType
from errors import OrbisimSemanticError
from orbsim_language.orbsim_ast.body_node import BodyNode
from orbsim_language.orbsim_type import OrbsimType
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
from orbsim_language.instance import Instance
@dataclass
class ExecuteVarInfo:
    name: str
    type: OrbsimType
    val: Any
@dataclass
class VariableInfo:
    name: str
    type: OrbsimType
    instance: 'Instance' = None

    def __eq__(self, other: 'VariableInfo') -> bool:
        return self.name == other.name


@dataclass
class FunctionInfo:
    name: str
    return_type: OrbsimType
    args: List[str]
    arg_types: List[OrbsimType]
    body: BodyNode =  None

    def __eq__(self, other: 'FunctionInfo') -> bool:
        return self.name == other.name and self.args == other.args

class Scope:
    '''
        Para la correcta definición de variables y 
        métodos(el contexto de las variables y métodos)
    '''

    def __init__(self, parent: 'Scope' = None):
        self.parent: 'Scope' = parent
        self.local_variables: Dict[str, VariableInfo] = {}
        self.local_functions: Dict[Tuple[str, int], FunctionInfo] = {}
    
    def check_var(self, var: str) -> bool: 
        '''
            Dice si una variable está definida o no en el programa
        '''
        if var in self.local_variables:
            return True
        if self.parent != None:
            return self.parent.check_var(var)
        return False
    

    def check_fun(self, fun: str, args: int)-> bool:
        if (fun, args) in self.local_functions:
            return True
        
        if self.parent != None:
            return self.parent.check_fun(fun, args)
        
        return False
    
    def define_var(self, var_id: str, type: OrbsimType) -> bool:
        if not self.check_var(var_id):
            self.local_variables[var_id] = VariableInfo(var_id, type)
            return True
        
        return False

    def define_fun(self, fun_name: str, return_type: OrbsimType, args: List[str], arg_types: List[OrbsimType], body) -> bool:
        if not self.check_fun(fun_name, len(args)):
            self.local_functions[(fun_name, len(args))] = FunctionInfo(fun_name, return_type, args, arg_types, body)
            return True
        return False
    
    def get_variable(self, identifier: str):
        if identifier in self.local_variables:
            return self.local_variables[identifier]
        if self.parent != None:
            return self.parent.get_variable(identifier)
    
    def create_child_scope(self):
        child_scope = Scope(self)
        return child_scope

class Context:
    '''
        Para la correcta definición de los tipos (contexto de los tipos)
    '''

    def __init__(self, parent: 'Context' = None): 
        self.types: Dict[str, Type] = {}
        self.local_functions: Dict[str, FunctionInfo] = {}
    
    def get_type(self, name: str):
        if name in self.types:
            return self.types[name]
        else:
            raise OrbisimSemanticError(f'El tipo {name} no se encuentra definido en el contexto')


        
    def create_type(self, name: str):
        if name in self.types:
            raise OrbisimSemanticError(f'Ya hay un tipo con el nombre {name} definido en el contexto')
        else:
            new_type = OrbsimType(name)
            self.types[name] = new_type
            return new_type
            
    def check_fun(self, fun: str, args: int):
        if (fun, args) in self.local_functions:
            return True
        return False
    
    def define_fun(self, fun_name: str, return_type: OrbsimType, args: List[str], arg_types: List[OrbsimType]) -> bool:
        if not self.check_fun(fun_name, len(args)):
            self.local_functions[(fun_name, len(args))] = FunctionInfo(fun_name, return_type, args, arg_types)
            return True
        return False
    
    def get_func(self, fun_name:str, params: int) -> FunctionInfo:
        if (fun_name, params) in self.local_functions:
            return self.local_functions[fun_name, params]
        raise OrbisimSemanticError(f'La función {fun_name} no está definida')