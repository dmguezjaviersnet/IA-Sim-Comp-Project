from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.statement_node import StatementNode
from orbsim_language.orbsim_ast.attribute_def import AttributeDef
from orbsim_language.orbsim_ast.method_def import MethodDef

@dataclass
class ClassDeclr(StatementNode):
    name: str
    attributes: List['AttributeDef']
    methods: List['MethodDef']
    parent: 'ClassDeclr' = None # por si hereda de otra clase (se acepta herencia simple)

