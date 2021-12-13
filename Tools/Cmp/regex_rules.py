from Own_symbol import Symbol
from Automata.astRegex import *

eval_rule = lambda rule, head, tail : rule(head, tail)

################################ E
# -> T X
def E_rule_rgx(head: Symbol, tail: list[Symbol]): 
    head.ast = tail[1].ast

def X_rule_rgx(head: Symbol, tail: list[Symbol]):
    tail[1].tmp = tail[0].ast

################################ X 
# -> | T X
def X0_rule_bar_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = tail[2].ast

def X1_rule_bar_rgx(head: Symbol, tail: list[Symbol]):
    tail[2].tmp = UnionNode(head.tmp, tail[1].ast)

# -> eps
def X0_rule_eps_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = head.tmp

############################### T -> F Y
def T_rule_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = tail[1].ast

def Y_rule_rgx(head: Symbol, tail: list[Symbol]):
    tail[1].tmp = tail[0].ast

############################### Y
# -> F Y
def Y0_rule_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = tail[1].ast

def Y1_rule_rgx(head: Symbol, tail: list[Symbol]):
    tail[1].tmp = ConcatNode(head.tmp, tail[0].ast)

# -> eps
def Y0_rule_eps_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = head.tmp

############################### F
# -> A P
def F_rule_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = tail[1].ast

def P_rule_AP_rgx(head: Symbol, tail: list[Symbol]):
    tail[1].tmp = tail[0].ast

############################### P
# -> M
def P_rule_M_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = tail[0].ast

# -> eps
def P_rule_eps_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = head.tmp

############################### M
# -> *
def M_rule_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = ClosureNode(head.tmp)

############################### A
# -> sym 
def A_rule_symbol_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = SymbolNode(tail[0].val)

# -> ( E )
def A_rule_brackets_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = tail[1].ast

# -> ε
def A_rule_eps_rgx(head: Symbol, tail: list[Symbol]):
    head.ast = EpsilonNode()