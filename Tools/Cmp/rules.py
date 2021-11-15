from own_symbol import Symbol
from ClassASTDesign.Number import Number
from ClassASTDesign.Sum import Sum
from ClassASTDesign.Sub import Sub
from ClassASTDesign.Mul import Mul
from ClassASTDesign.Div import Div

eval_rule = lambda rule, head, tail : rule(head, tail)

################################ E -> T X
def E_rule(head: Symbol, tail: list[Symbol]): 
    head.ast = tail[1].ast

def X_rule(head: Symbol, tail: list[Symbol]):
    tail[1].tmp = tail[0].ast

################################ X 
# -> + T X
def X0_rule_plus(head: Symbol, tail: list[Symbol]):
    head.ast = tail[2].ast

def X1_rule_plus(head: Symbol, tail: list[Symbol]):
    tail[2].tmp = Sum(head.tmp, tail[1].ast)


# -> - T X
def X0_rule_minus(head: Symbol, tail: list[Symbol]):
    head.ast = tail[2].ast

def X1_rule_minus(head: Symbol, tail: list[Symbol]):
    tail[2].tmp = Sub(head.tmp, tail[1].ast)

# -> eps
def X0_rule_eps(head: Symbol, tail: list[Symbol]):
    head.ast = head.tmp


############################### T -> F Y
def T_rule(head: Symbol, tail: list[Symbol]):
    head.ast = tail[1].ast

def Y_rule(head: Symbol, tail: list[Symbol]):
    tail[1].tmp = tail[0].ast

############################### Y
# -> * F Y
def Y0_rule_mul(head: Symbol, tail: list[Symbol]):
    head.ast = tail[2].ast

def Y1_rule_mul(head: Symbol, tail: list[Symbol]):
    tail[2].tmp = Mul(head.tmp, tail[1].ast)

# -> / F Y
def Y0_rule_div(head: Symbol, tail: list[Symbol]):
    head.ast = tail[2].ast

def Y1_rule_div(head: Symbol, tail: list[Symbol]):
    tail[2].tmp = Div(head.tmp, tail[1].ast)

# -> eps
def Y0_rule_eps(head: Symbol, tail: list[Symbol]):
    head.ast = head.tmp

############################### F
# -> ( E )
def F_rule_brackets(head: Symbol, tail: list[Symbol]):
    head.ast = tail[1].ast

# -> i
def F_rule_i(head: Symbol, tail: list[Symbol]):
    head.ast = Number(tail[0].val)