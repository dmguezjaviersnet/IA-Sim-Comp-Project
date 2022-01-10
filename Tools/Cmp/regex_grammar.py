from Grammar import Grammar
from regex_rules import*
from Terminal import*

from Non_terminal import*
from Production import*
# Terminales
clousure = Terminal('*')
openb = Terminal('(')
closedb = Terminal(')')
bar = Terminal('|')
character = Terminal('character', 'val')
empty = Terminal('eps')
regex_empty = Terminal('ε')
eof = Terminal('$')
terminals = [clousure, bar, openb, closedb, character, regex_empty, empty, eof]


# No terminales
E = Non_terminal('E', 'ast')
X = Non_terminal('X', 'ast', 'tmp')
T = Non_terminal('T', 'ast', 'tmp')
Y = Non_terminal('Y', 'ast', 'tmp')
F = Non_terminal('F', 'ast')
P = Non_terminal('P', 'ast')
M = Non_terminal('M', 'ast', 'tmp')
A = Non_terminal('A', 'ast')
nts = [E, X, T, Y, F, P, M, A]


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
                [[clousure]],
                [[(M_rule_rgx, True)]]
                )

p8 = Production(A, 
                [[character], [openb, E, closedb], [regex_empty]],
                [[(A_rule_symbol_rgx, True)], [(A_rule_brackets_rgx, True)], [(A_rule_eps_rgx, True)]]
                )

prods = [p1, p2, p3, p4, p5, p6, p7, p8]

regex_grammar = Grammar(terminals, nts, E, prods)