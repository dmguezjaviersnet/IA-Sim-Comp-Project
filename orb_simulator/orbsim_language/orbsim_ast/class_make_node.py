from dataclasses import dataclass
from typing import List
from orbsim_language.orbsim_ast.expression_node import ExpressionNode
# from orbsim_language.orbsim_ast.attribute_def_node import AttributeDef
# from orb_simulator.orbsim_language.orbsim_ast.method_declr_node import MethodDef

@dataclass
class ClassMakeNode(ExpressionNode):
    classname: str
    params: List[ExpressionNode]

