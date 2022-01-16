from Grammar import Grammar
from regex_rules import*
from Terminal import*

from Non_terminal import*
from Production import*

'''
   Gramática de Expresiones Regulares
   E -> T X
   X -> '|' T X
      | epsilon
   T -> F Y
   Y -> F Y 
      | epsilon
   F -> A P
   P -> M
      | epsilon
   M -> *
      | ?
      | +
      | epsilon
   A -> symbol
      | (E)
      | [W]
      | ε
   W -> R S
   S -> W
      | epsilon
   R -> B Q
   Q -> - B Q
      | epsilon
   B -> symbol
   C -> symbol  

'''
# Terminales
clousure = Terminal('*')
question = Terminal('?')
rplus = Terminal('+')
rrange = Terminal('-') 
openb = Terminal('(')
closedb = Terminal(')')
opensb = Terminal('[')
closedsb = Terminal(']')
bar = Terminal('|')
character = Terminal('character', 'val')
empty = Terminal('eps')
regex_empty = Terminal('ε')
eof = Terminal('$')
terminals = [clousure, question, rrange, rplus, bar, openb, closedb, opensb, closedsb, character, regex_empty, empty, eof]


# No terminales
E = Non_terminal('E', 'ast')
X = Non_terminal('X', 'ast', 'tmp')
T = Non_terminal('T', 'ast', 'tmp')
Y = Non_terminal('Y', 'ast', 'tmp')
F = Non_terminal('F', 'ast')
P = Non_terminal('P', 'ast')
M = Non_terminal('M', 'ast', 'tmp')
A = Non_terminal('A', 'ast')
W = Non_terminal('W', 'ast')
R = Non_terminal('R', 'ast', 'tmp')
S = Non_terminal('S', 'ast', 'tmp')
B = Non_terminal('B', 'ast', 'tmp')
C = Non_terminal('C', 'ast', 'tmp')
Q = Non_terminal('Q', 'ast', 'tmp')


nts = [E, X, T, Y, F, P, M, A, W, R, S, B, C, Q]


# Producciones
p1 = Production(E, 
                [[T, X]],
                [[(E_rule_rgx, True), (X_rule_rgx, False)]]
               )

p2 = Production(X, 
                [[bar, T, X], [empty]],
                [[(X0_rule_bar_rgx, True), (X1_rule_bar_rgx, False)], [(X0_rule_eps_rgx, True)]]
               )

p3 = Production(T, 
                [[F, Y]], 
                [[(T_rule_rgx, True), (Y_rule_rgx, False)]]
               )

p4 = Production(Y, 
                [[F, Y], [empty]],
                [[(Y0_rule_rgx, True), (Y1_rule_rgx, False)], [(Y0_rule_eps_rgx, True)]]
               )

p5 = Production(F, 
                [[A, P]],
                [[(F_rule_rgx, True), (P_rule_AP_rgx, False)]]
               )

p6 = Production(P, 
                [[M], [empty]],
                [[(P_rule_M_1_rgx, True), (P_rule_M_2_rgx, False)], [(P_rule_eps_rgx, True)]]
                )

p7 = Production(M, 
                [[clousure], [question], [rplus]],
                [[(M_rule_rgx, True)],[(M_rule_question, True)],[(M_rule_plus, True)]]
               )

p8 = Production(A, 
                [[character], [openb, E, closedb], [opensb, W, closedsb], [regex_empty]],
                [[(A_rule_symbol_rgx, True)], [(A_rule_brackets_rgx, True)], [(A_rule_square_brackets_rgx, True)], [(A_rule_eps_rgx, True)]]
               )

p9 = Production(W,
               [[R, S]],
               [[(W_rule_rgx, True), (S1_rule_rgx, False)]]
               )

p10 = Production(S,
               [[R, S], [empty]],
               [[(S2_rule_rgx, False), (S3_rule_rgx, True)], [(S4_rule_rgx, True)]]
               )

p11 = Production(R,
               [[B, Q]],
               [[(Q1_rule_rgx, False), (R1_rule_rgx, True)]]
               )

p12 = Production(Q,
               [[rrange, B, Q], [empty]],
               [[(B1_rule_rgx, False), (Q2_rule_rgx, True)], [(Q3_rule_rgx, True)]]
               )

p13 = Production(B,
               [[character]],
               [[(B_rule_symbol_rgx, True)]]
               )

p14 = Production(C,
               [[character]],
               [[(C_rule_symbol_rgx, True)]]
               )

prods = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13]

regex_grammar = Grammar(terminals, nts, E, prods)