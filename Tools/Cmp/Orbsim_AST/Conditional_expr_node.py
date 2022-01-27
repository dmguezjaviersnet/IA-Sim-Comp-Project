from ExpressionNode import ExpressionNode
from dataclasses import dataclass

<<<<<<< HEAD:Tools/Cmp/AST_SL/ConditionalExprNode.py
=======


>>>>>>> 1b4cb44d312d0599c758dbf5b303aac308c96332:Tools/Cmp/Orbsim_AST/Conditional_expr_node.py
@dataclass
class ConditionalExprNode(ExpressionNode):
    if_expr: ExpressionNode
    then_expr: ExpressionNode
    else_expr: ExpressionNode