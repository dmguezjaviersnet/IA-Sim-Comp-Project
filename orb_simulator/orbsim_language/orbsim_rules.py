from typing import List
from parser.own_symbol import Symbol
from orbsim_language.orbsim_ast import ProgramNode, StatementNode, VariableDeclrNode
from orbsim_language.orbsim_ast import FuncDeclrNode, ConditionalNode, LoopNode
from orbsim_language.orbsim_ast import OrNode, AndNode, GreaterEqualNode, LessEqualNode
from orbsim_language.orbsim_ast import GreaterThanNode, LessThanNode, EqualNode, NotEqualNode
from orbsim_language.orbsim_ast import VariableNode, RetNode
from orbsim_language.orbsim_ast import NotNode, PlusNode, MinusNode, FloatNode, IntegerNode
from orbsim_language.orbsim_ast import ProductNode, DivNode, AtomicNode
from orbsim_language.orbsim_ast import FunCallNode, ModNode

def program_rule(head: Symbol, tail: List[Symbol]):
    head.ast = ProgramNode(tail[0].ast)

def stmt_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast

def stmt_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]

def stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def let_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = VariableDeclrNode(tail[1].val, tail[3].ast)

def ret_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = RetNode(tail[1].ast)

def def_func_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = FuncDeclrNode(tail[1].val, [elem for elem in tail[3].ast], tail[6].ast)

def loop_rule(head: Symbol, tail: List[Symbol]):
    head.ast = LoopNode(tail[2].ast, tail[5].ast)

def conditional_stmt_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = ConditionalNode(tail[2].ast, tail[6].ast, None)

def conditional_stmt_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = ConditionalNode(tail[2].ast, tail[6].ast, tail[10].ast)

def arg_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].val] + tail[2].ast

def arg_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].val]

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

def atom_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = IntegerNode(tail[0].val)

def atom_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = FloatNode(tail[0].val)
    
def atom_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = AtomicNode(tail[0].val)

def atom_rule4(head: Symbol, tail: List[Symbol]):
    head.ast = AtomicNode(tail[0].val)

def atom_rule5(head: Symbol, tail: List[Symbol]):
    head.ast = AtomicNode(tail[0].val)

def atom_rule6(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def func_call_rule(head: Symbol, tail: List[Symbol]):
    head.ast = FunCallNode(tail[0].val, tail[2].ast)

def expr_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast

def expr_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]