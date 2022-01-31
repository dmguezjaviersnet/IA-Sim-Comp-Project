from dataclasses import dataclass
from typing import List
from statement_node import StatementNode
from attribute_def import AttributeDef
from method_def import MethodDef
@dataclass
class ClassDeclr(StatementNode):
    name: str
    attributes: List['AttributeDef']
    methods: List['MethodDef']
    parent: 'ClassDeclr' = None # por si hereda de otra clase (se acepta herencia simple)

