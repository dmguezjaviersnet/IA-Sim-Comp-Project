from typing import List
from test_language.testing_ast import Number, Sum
from test_language.testing_ast import Sub, Mul, Div
from parser.own_symbol import Symbol

################################ E
# -> T + X
def E1_rule(head: Symbol, tail: List[Symbol]):
    head.ast = Sum(tail[0].ast, tail[2].ast)

# -> T - X
def E2_rule(head: Symbol, tail: List[Symbol]):
    head.ast = Sub(tail[0].ast, tail[2].ast)

# -> T
def E3_rule(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

############################### T
# -> F * T
def T1_rule(head: Symbol, tail: List[Symbol]):
    head.ast = Mul(tail[0].ast, tail[2].ast)

# -> F / T
def T2_rule(head: Symbol, tail: List[Symbol]):
    head.ast = Div(tail[0].ast, tail[2].ast)

# -> F
def T3_rule(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

############################### F
# -> ( E )
def F1_rule(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

# -> i
def F2_rule(head: Symbol, tail: List[Symbol]):
    head.ast = Number(tail[0].val)