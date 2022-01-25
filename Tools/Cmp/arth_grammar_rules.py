from typing import Callable, List
from Own_symbol import Symbol
from ClassASTDesign.Number import Number
from ClassASTDesign.Sum import Sum
from ClassASTDesign.Sub import Sub
from ClassASTDesign.Mul import Mul
from ClassASTDesign.Div import Div
from Non_terminal import Non_terminal

def eval_rule(rule: Callable, head: Non_terminal, tail: List[Symbol]):
    rule(head, tail)

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