from dataclasses import dataclass
from typing import List


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


class Context:

    def __init__(self, parent: 'Context' = None):
        self.parent: 'Context' = parent
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

    def create_child_context(self):
        child_context = Context(self)
        return child_context
