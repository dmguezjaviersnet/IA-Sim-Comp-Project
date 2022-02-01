from typing import List
from parser.own_symbol import Symbol
from orbsim_language.orbsim_ast import ProgramNode, StatementNode, VariableDeclr
from orbsim_language.orbsim_ast import FuncDeclr, ConditionalExprNode, LoopExprNode
from orbsim_language.orbsim_ast import OrNode, AndNode, GreaterEqual, LessEqual
from orbsim_language.orbsim_ast import GreaterThanNode, LessThanNode, EqualNode, NotEqualNode
from orbsim_language.orbsim_ast import FuncDeclr, ConditionalExprNode, LoopExprNode
from orbsim_language.orbsim_ast import FuncDeclr, ConditionalExprNode, LoopExprNode
from orbsim_language.orbsim_ast import VariableNode
from orbsim_language.orbsim_ast import NotNode, PlusNode, MinusNode, FloatNode, IntegerNode
from orbsim_language.orbsim_ast import ProductNode, DivNode, AtomicNode
from orbsim_language.orbsim_ast import FunCall, ModNode

def program_rule(head: Symbol, tail: List[Symbol]):
    head.ast = ProgramNode(tail.ast)

def stmt_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [StatementNode()] + tail[1].ast

def stmt_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [StatementNode()]

def stmt_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def stmt_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def stmt_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def stmt_rule4(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def stmt_rule5(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def let_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = VariableDeclr(tail[1].val, tail[3].ast)

def def_func_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = FuncDeclr(tail[1].val, [elem for elem in tail[3]], tail[6].ast)

def loop_rule(head: Symbol, tail: List[Symbol]):
    head.ast = LoopExprNode(tail[2].ast, tail[5].ast)

def conditional_stmt_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = ConditionalExprNode(tail[2].ast, tail[6].ast, tail[10].ast)

def conditional_stmt_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = ConditionalExprNode(tail[2].ast, tail[6].ast, None)

def arg_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[2].val] + tail[0].ast

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
        head.ast = GreaterEqual(tail[0].ast, tail[2].ast)
    
    elif tail[1].ast == '<=':
        head.ast = LessEqual(tail[0].ast, tail[2].ast)
    
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
    head.ast = VariableNode(tail[0].val)

def func_call_rule(head: Symbol, tail: List[Symbol]):
    head.ast = FunCall(tail[0].val, tail[2].ast)

def expr_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast

def expr_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]