from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.statement_node import StatementNode
from orbsim_language.orbsim_ast.attribute_declr_node import AttributeDeclrNode
from orbsim_language.orbsim_ast.method_declr_node import MethodDeclrNode

@dataclass
class ClassDeclrNode(StatementNode):
    name: str
    attributes: List['AttributeDeclrNode']
    methods: List['MethodDeclrNode']
    parent: 'ClassDeclrNode' = None # por si hereda de otra clase (se acepta herencia simple)

