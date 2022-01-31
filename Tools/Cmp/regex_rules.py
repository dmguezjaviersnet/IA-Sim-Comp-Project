from typing import List
from own_symbol import Symbol

from regex_ast import ClosureNode, ConcatNode, RangeNode
from regex_ast import EpsilonNode, SymbolNode, UnionNode

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

############################### A
# -> character 
def A_rule_character_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = SymbolNode(tail[0].ast)

# -> ( E )
def A_rule_brackets_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

# -> [ W ]
def A_rule_square_brackets_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

# -> ε
def A_rule_eps_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = EpsilonNode(tail[0].identifier)

# -> \\n
def A_rule_new_line(head: Symbol, tail: List[Symbol]):
    head.ast = SymbolNode(tail[0].identifier)

################################ character
# -> except_metas

def character_rule_except_metas(head: Symbol, tail: List[Symbol]):
    head.ast = tail[0].val

# \ except_specials
def character_rule_except_specials(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].val

################################ W
# -> R S
def W_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

def S1_rule_rgx(head: Symbol, tail: List[Symbol]):
    tail[1].tmp = tail[0].ast

################################ S
# -> R S
def S2_rule_rgx(head: Symbol, tail: List[Symbol]):
    tail[1].tmp = tail[0].ast

def S3_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

# -> eps
def S4_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = head.tmp

################################ R
# -> B Q
def Q1_rule_rgx(head: Symbol, tail: List[Symbol]):
    tail[1].tmp = tail[0].ast

def R1_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[1].ast

################################ Q

# -> - B Q
def B1_rule_rgx(head: Symbol, tail: List[Symbol]):
    tail[2].tmp = RangeNode(head.tmp, tail[1].ast)

def Q2_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = tail[2].ast

# -> eps
def Q3_rule_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = head.tmp

############################### B
# -> character
def B_rule_character_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = SymbolNode(tail[0].ast)

############################### C
# -> character
def C_rule_character_rgx(head: Symbol, tail: List[Symbol]):
    head.ast = SymbolNode(tail[0].ast)

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
    
# -> ?
def M_rule_question(head: Symbol, tail: List[Symbol]):
    head.ast = UnionNode(head.tmp, EpsilonNode('ε'))

# -> +
def M_rule_plus(head: Symbol, tail: List[Symbol]):
    head.ast = ConcatNode(head.tmp, ClosureNode(head.tmp))
