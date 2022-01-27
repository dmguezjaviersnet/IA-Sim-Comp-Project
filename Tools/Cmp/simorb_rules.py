from typing import Callable, List
from Non_terminal import Non_terminal
from Own_symbol import Symbol

from Tools.Cmp.Orbsim_AST.Program_node import ProgramNode
from Tools.Cmp.Orbsim_AST.Statement_node import StatementNode
from Tools.Cmp.Orbsim_AST.Let_variable import LetVariable
from Tools.Cmp.Orbsim_AST.Def_func import DefFunc
from Tools.Cmp.Orbsim_AST.Conditional_expr_node import ConditionalExprNode
from Tools.Cmp.Orbsim_AST.Loop_expr_node import LoopExprNode
from Tools.Cmp.Orbsim_AST.Not_node import NotNode
from Tools.Cmp.Orbsim_AST.Plus_node import PlusNode
from Tools.Cmp.Orbsim_AST.Minus_node import MinusNode
from Tools.Cmp.Orbsim_AST.Times_node import TimesNode
from Tools.Cmp.Orbsim_AST.Div_node import DivNode
from Tools.Cmp.Orbsim_AST.Atomic_node import AtomicNode
from Tools.Cmp.Orbsim_AST.Fun_call import FunCall
from Tools.Cmp.Orbsim_AST.Mod_node import Mod_node


def eval_rule(rule: Callable, head: Non_terminal, tail: List[Symbol]):
    rule(head, tail)

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
    head.ast = LetVariable(tail[1].val, tail[3].ast)

def def_func_stmt_rule(head: Symbol, tail: List[Symbol]):
    head.ast = DefFunc(tail[1].val, [elem for elem in tail[3]], tail[6].ast)

def loop_rule(head: Symbol, tail: List[Symbol]):
    head.ast = LoopExprNode(tail[2].ast, tail[5].ast)

def conditional_stmt_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = ConditionalExprNode(tail[2].ast, tail[6].ast, tail[10].ast)

def conditional_stmt_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = ConditionalExprNode(tail[2].ast, tail[6].ast, None)

def arg_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].val] + tail[1].val

def arg_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].val]

def expression_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def expression_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def unary_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = NotNode(tail[1].ast)

def binary_expr_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = PlusNode(tail[0].ast, tail[2].ast)

def binary_expr_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = MinusNode(tail[0].ast, tail[2].ast)

def binary_expr_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def term_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = TimesNode(tail[0].ast, tail[2].ast)

def term_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = DivNode(tail[0].ast, tail[2].ast)

def term_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = Mod_node(tail[0].ast, tail[2].ast)

def term_rule4(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def factor_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def factor_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

def atom_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = AtomicNode(tail[0].val)
    
def atom_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = AtomicNode(tail[0].val)

def atom_rule3(head: Symbol, tail: List[Symbol]):
    head.ast = AtomicNode(tail[0].val)

def atom_rule4(head: Symbol, tail: List[Symbol]):
    head.ast = AtomicNode(tail[0].val)

def atom_rule5(head: Symbol, tail: List[Symbol]):
    head.ast = AtomicNode(tail[0].ast)

def func_call_rule(head: Symbol, tail: List[Symbol]):
    head.ast = FunCall(tail[0].val, tail[2].ast)

def expr_list_rule1(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast] + tail[2].ast

def expr_list_rule2(head: Symbol, tail: List[Symbol]):
    head.ast = [tail[0].ast]