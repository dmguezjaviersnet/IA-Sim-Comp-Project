from typing import List

from parser.own_symbol import Symbol
from orbsim_language.orbsim_ast import ProgramNode, VariableDeclrNode, FuncDeclrNode, MethodDeclrNode
from orbsim_language.orbsim_ast import ConditionalNode, LoopNode, OrNode, AndNode, ContinueNode, BreakNode
from orbsim_language.orbsim_ast import GreaterEqualNode, LessEqualNode, GreaterThanNode
from orbsim_language.orbsim_ast import LessThanNode, EqualNode, NotEqualNode, RetNode
from orbsim_language.orbsim_ast import AssingNode, AttributeDeclrNode, NotNode, PlusNode, NegNumberNode
from orbsim_language.orbsim_ast import MinusNode, FloatNode, IntegerNode, ProductNode, StringNode, BooleanNode
from orbsim_language.orbsim_ast import DivNode, PrintNode, FunCallNode, ModNode, ListCreationNode, StopSimNode, StartSimNode, PauseSimNode
from orbsim_language.orbsim_ast import BitwiseAndNode, BitwiseOrNode, BitwiseXorNode, BitwiseShiftRightNode, BitwiseShiftLeftNode
from orbsim_language.orbsim_ast import ClassDeclrNode, VariableNode, BodyNode, ClassMakeNode, MethodCallNode, AttributeCallNode
from orbsim_language.orbsim_ast import DrawquadtreeNode
from orbsim_language.orbsim_ast import AnimateEarthNode, ShowOrbitsNode
from orbsim_language.orbsim_ast import SpaceDebrisNode, SatelliteNode, OrbitNode, AgentNode
from orbsim_language.orbsim_ast import TupleCreationNode

def program_rule(head: Symbol, tail: List[Symbol]):
    head.ast = ProgramNode(tail[0].ast)

def stmt_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast

def stmt_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]

def stmt_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = ClassDeclrNode(tail[1].val, [elem for elem in tail[3].ast if isinstance(elem, AttributeDeclrNode)],
                        [elem for elem in tail[3].ast if isinstance(elem, MethodDeclrNode)]
                        ) 

def stmt_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def class_body_stmt_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast
 
def class_body_stmt_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]

def class_body_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def attr_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = AttributeDeclrNode(tail[1].val, tail[0]. val)

def def_method_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = MethodDeclrNode(tail[2].val, tail[1].val, [id_param for id_param, _ in tail[4].ast],
                            [type_param for _, type_param in tail[4].ast], 
                            BodyNode([elem for elem in tail[7].ast])
                            )

def def_func_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = FuncDeclrNode(tail[2].val, tail[1].val, [id_param for id_param, _ in tail[4].ast],
                            [type_param for _, type_param in tail[4].ast], 
                            BodyNode([elem for elem in tail[7].ast])
                            )

def func_body_stmt_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast
 
def func_body_stmt_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]

def func_body_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def let_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = VariableDeclrNode(tail[2].val, tail[1].val, tail[4].ast)

def assign_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = AssingNode(tail[0].val, tail[2].ast)

def loop_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = LoopNode(tail[2].ast, BodyNode(tail[5].ast))

def loop_body_stmt_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast
 
def loop_body_stmt_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]

def loop_body_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def flow_stmt_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = ContinueNode()

def flow_stmt_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = BreakNode()

def conditional_stmt_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = ConditionalNode(tail[2].ast, BodyNode(tail[6].ast), None)

def conditional_stmt_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = ConditionalNode(tail[2].ast, BodyNode(tail[6].ast), BodyNode(tail[10].ast))

def conditional_body_stmt_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast

def conditional_body_stmt_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]

def conditional_body_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def ret_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = RetNode(tail[1].ast)

def print_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = PrintNode(tail[1].ast)

def start_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = StartSimNode()

def stop_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = StopSimNode()

def pause_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = PauseSimNode()

def drawquadtree_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = DrawquadtreeNode()

def animate_earth_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = AnimateEarthNode()

def show_orbits_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = ShowOrbitsNode()

def print_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = PrintNode(tail[1].ast)

def arg_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [(tail[1].val, tail[0].val)] + tail[3].ast

def arg_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [(tail[1].val, tail[0].val)]

def arg_list_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = []

def expression_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def or_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = OrNode(tail[0].ast, tail[2].ast)

def or_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def and_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = AndNode(tail[0].ast, tail[2].ast)

def and_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def not_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = NotNode(tail[1].ast)

def not_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def compare_expr_rule1(head: Symbol, tail: List[Symbol]):
    if tail[1].ast == '>':
        head.ast = GreaterThanNode(tail[0].ast, tail[2].ast)
    
    elif tail[1].ast == '<':
        head.ast = LessThanNode(tail[0].ast, tail[2].ast)
    
    elif tail[1].ast == '>=':
        head.ast = GreaterEqualNode(tail[0].ast, tail[2].ast)
    
    elif tail[1].ast == '<=':
        head.ast = LessEqualNode(tail[0].ast, tail[2].ast)
    
    elif tail[1].ast == '==':
        head.ast = EqualNode(tail[0].ast, tail[2].ast)
    
    elif tail[1].ast == '!=':
        head.ast = NotEqualNode(tail[0].ast, tail[2].ast)

def compare_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def compare_op_rule(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].identifier

def bitwise_or_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = BitwiseOrNode(tail[0].ast, tail[2].ast)

def bitwise_or_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def bitwise_xor_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = BitwiseXorNode(tail[0].ast, tail[2].ast)

def bitwise_xor_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def bitwise_and_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = BitwiseAndNode(tail[0].ast, tail[2].ast)

def bitwise_and_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def bitwise_shift_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = BitwiseShiftLeftNode(tail[0].ast, tail[2].ast)

def bitwise_shift_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = BitwiseShiftRightNode(tail[0].ast, tail[2].ast)

def bitwise_shift_expr_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def arth_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = PlusNode(tail[0].ast, tail[2].ast)

def arth_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = MinusNode(tail[0].ast, tail[2].ast)

def arth_expr_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def term_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = ProductNode(tail[0].ast, tail[2].ast)

def term_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = DivNode(tail[0].ast, tail[2].ast)

def term_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = ModNode(tail[0].ast, tail[2].ast)

def term_rule4(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def factor_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def factor_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

def factor_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = NegNumberNode(tail[1].ast)

def factor_rule4(head: Symbol, tail: List[Symbol]):
    head.ast = TupleCreationNode(tail[1].ast)

def atom_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = IntegerNode(tail[0].val)

def atom_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = FloatNode(tail[0].val)
    
def atom_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = BooleanNode(tail[0].val)

def atom_rule4(head: Symbol, tail: List[Symbol]):
    head.ast = StringNode(tail[0].val)

def atom_rule5(head: Symbol, tail: List[Symbol]):
    head.ast = VariableNode(tail[0].val)

def atom_rule6(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def atom_rule7(head: Symbol, tail: List[Symbol]):
    head.ast = OrbitNode(tail[0].val)

def atom_rule8(head: Symbol, tail: List[Symbol]):
    head.ast = SpaceDebrisNode(tail[0].val)

def atom_rule9(head: Symbol, tail: List[Symbol]):
    head.ast = SatelliteNode(tail[0].val)

def atom_rule10(head: Symbol, tail: List[Symbol]):
    head.ast = AgentNode(tail[0].val)

def list_creation_rule(head: Symbol, tail: List[Symbol]):
    head.ast = ListCreationNode(tail[1].ast)

def tuple_creation_rule(head: Symbol, tail: List[Symbol]):
    head.ast = TupleCreationNode(tail[2].ast)

def func_call_rule(head: Symbol, tail: List[Symbol]):
    head.ast = FunCallNode(tail[0].val, tail[2].ast)

def make_rule(head: Symbol, tail: List[Symbol]):
    head.ast = ClassMakeNode(tail[1].val, tail[3].ast)

def method_call_rule(head: Symbol, tail: List[Symbol]):
    head.ast = MethodCallNode(tail[0].val, tail[2].val, tail[4].ast)

def attr_call_rule(head: Symbol, tail: List[Symbol]):
    head.ast = AttributeCallNode(tail[0].val, tail[2].val)

def expr_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast

def expr_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]

def expr_list_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = []