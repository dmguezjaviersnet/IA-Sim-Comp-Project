from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.statement_node import StatementNode
from orbsim_language.orbsim_ast.attribute_def_node import AttributeDef
from orb_simulator.orbsim_language.orbsim_ast.method_declr_node import MethodDef

@dataclass
class ClassDeclrNode(StatementNode):
    name: str
    attributes: List['AttributeDef']
    methods: List['MethodDef']
    parent: 'ClassDeclrNode' = None # por si hereda de otra clase (se acepta herencia simple)

