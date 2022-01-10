from Own_symbol import Symbol
from astRegex import *

################################ E
# -> T X
def E_rule_rgx(head: Symbol, tail: List[Symbol]): 
    head.ast = tail[1].ast

def X_rule_rgx(head: Symbol, tail: List[Symbol]):
    tail[1].tmp = tail[0].ast

################################ X 
# -> | T X
def X0_rule_bar_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[2].ast

def X1_rule_bar_rgx(head: Symbol, tail: List[Symbol]):
    tail[2].tmp = UnionNode(head.tmp, tail[1].ast)

# -> eps
def X0_rule_eps_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = head.tmp

############################### T -> F Y
def T_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

def Y_rule_rgx(head: Symbol, tail: List[Symbol]):
    tail[1].tmp = tail[0].ast

############################### Y
# -> F Y
def Y0_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

def Y1_rule_rgx(head: Symbol, tail: List[Symbol]):
    tail[1].tmp = ConcatNode(head.tmp, tail[0].ast)

# -> eps
def Y0_rule_eps_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = head.tmp

############################### F
# -> A P
def F_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

def P_rule_AP_rgx(head: Symbol, tail: List[Symbol]):
    tail[1].tmp = tail[0].ast

############################### P
# -> M
def P_rule_M_1_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].ast

def P_rule_M_2_rgx(head: Symbol, tail: List[Symbol]):
    tail[0].tmp = head.tmp


# -> eps
def P_rule_eps_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = head.tmp

############################### M
# -> *
def M_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = ClosureNode(head.tmp)

############################### A
# -> sym 
def A_rule_symbol_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = SymbolNode(tail[0].val)

# -> ( E )
def A_rule_brackets_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

# -> ε
def A_rule_eps_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = EpsilonNode(tail[0].identifier)