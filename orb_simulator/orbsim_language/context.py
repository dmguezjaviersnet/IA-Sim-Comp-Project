from dataclasses import dataclass
from typing import Any, Dict, List, Type
# from orbsim_language.orbsim_type import OrbsimType
from errors import OrbisimSemanticError
from orbsim_language.orbsim_type import OrbsimType
from orbsim_language.orbsim_ast.expression_node import ExpressionNode

@dataclass
class ExecuteVarInfo:
    name: str
    type: OrbsimType
    val: Any
@dataclass
class VariableInfo:
    name: str
    type: OrbsimType
    expr: ExpressionNode

    def __eq__(self, other: 'VariableInfo') -> bool:
        return self.name == other.name


@dataclass
class FunctionInfo:
    name: str
    return_type: OrbsimType
    args: List[str]
    arg_types: List[OrbsimType]

    def __eq__(self, other: 'FunctionInfo') -> bool:
        return self.name == other.name and self.args == other.args

class ExScope:
    '''
        Para la correcta definición de variables y 
        métodos(el contexto de las variables y métodos)
    '''

    def __init__(self, parent: 'ExScope' = None):
        self.parent: 'ExScope' = parent
        self.local_variables: Dict[str, ExecuteVarInfo] = {}
        self.local_functions = {}
    
    def check_var(self, var: str) -> bool: 
        '''
            Dice si una variable está definida o no en el programa
        '''
        if var  in self.local_variables:
            return True
        if self.parent != None:
            return self.parent.check_var(var)
        return False
    

    def check_fun(self, fun: str, args: int):
        if (fun, args) in self.local_functions:
            return True
        
        if self.parent != None:
            return self.parent.check_fun(fun, args)
        
        return False
    
    def define_var(self, var_id: str, type: OrbsimType, val: Any) -> bool:
        if not self.check_var(var_id):
            self.local_variables[var_id] = ExecuteVarInfo(var_id, type, val)
            return True
        
        return False

    def define_fun(self, fun_name: str, return_type: OrbsimType, args: List[str], arg_types: List[OrbsimType]) -> bool:
        if not self.check_fun(fun_name, len(return_type)):
            self.local_functions[(fun_name, len(args))] = FunctionInfo(fun_name, return_type, args, arg_types)
            return True
        return False
    
    def get_variable_val(self, var_name: str):
        if var_name in self.local_variables:
            return self.local_variables[var_name].val
        if self.parent != None:
             return self.parent.get_variable_val(var_name)
    
    def assing_new_variable_val(self, var_name: str, new_value):
        if var_name in self.local_variables:
            self.local_variables[var_name].val = new_value
            return True
        if self.parent != None:
            return self.parent.assing_new_variable_val(var_name, new_value)
        return False

    def create_child_scope(self):
        child_scope = ExScope(self)
        return child_scope


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
        '''
            Dice si una variable está definida o no en el programa
        '''
        if var  in self.local_variables:
            return True
        if self.parent != None:
            return self.parent.check_var(var)
        return False
    

    def check_fun(self, fun: str, args: int):
        if (fun, args) in self.local_functions:
            return True
        
        if self.parent != None:
            return self.parent.check_fun(fun, args)
        
        return False
    
    def define_var(self, var_id: str, type: OrbsimType, expr: 'ExpressionNode') -> bool:
        if not self.check_var(var_id):
            self.local_variables[var_id] = VariableInfo(var_id, type, expr)
            return True
        
        return False

    def define_fun(self, fun_name: str, return_type: OrbsimType, args: List[str], arg_types: List[OrbsimType]) -> bool:
        if not self.check_fun(fun_name, len(return_type)):
            self.local_functions[(fun_name, len(args))] = FunctionInfo(fun_name, return_type, args, arg_types)
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
        self.types: Dict[str, Type] = {}
        
    
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
            
