from lexer.regex_rules import *
from parser.grammar import Grammar
from parser.terminal import Terminal, Epsilon, Eof
from parser.non_terminal import Non_terminal
from parser.production import Production

'''
   Gramática de Expresiones Regulares
   E -> T X
   X -> '|' T X
      | epsilon
   T -> F Y
   Y -> F Y 
      | epsilon
   F -> A P
   A -> character
      | ( E )
      | [ W ]
      | ε
      | \\n
   W -> R S
   S -> R S
      | epsilon
   R -> B Q
   Q -> - B Q
      | epsilon
   B -> character
   C -> character
   character -> any_character_except_metas
         | '\\' any_character_except_specials

   P -> M
      | epsilon
   M -> *
      | ?
      | +


   specialcharacters
   (  metacharacters -> (  * - + , ( ) [ ] { } ^ | ?  )
   -> ! " # $ % & ' . / : ; < = > @ \ _ ` ~  )

   anycharacter -> 0 1 2 3 4 5 6 7 8 9
               A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
               a b c d e f g h i j k l m n o p q r s t u v w x y z

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
regex_empty = Terminal('ε')
any_character = Terminal('any_character')
literal = Terminal('\\')
new_line = Terminal('\n')
empty = Epsilon()
eof = Eof()
terminals = [clousure, question, rrange, rplus, bar, openb, closedb, opensb,
             closedsb, any_character, new_line, literal, regex_empty, empty, eof]


# No terminales
E = Non_terminal('E', 'ast')
X = Non_terminal('X', 'ast', 'tmp')
T = Non_terminal('T', 'ast', 'tmp')
Y = Non_terminal('Y', 'ast', 'tmp')
F = Non_terminal('F', 'ast')
P = Non_terminal('P', 'ast')
M = Non_terminal('M', 'ast', 'tmp')
A = Non_terminal('A', 'ast')
character = Non_terminal('character', 'ast')
W = Non_terminal('W', 'ast')
R = Non_terminal('R', 'ast', 'tmp')
S = Non_terminal('S', 'ast', 'tmp')
B = Non_terminal('B', 'ast', 'tmp')
C = Non_terminal('C', 'ast', 'tmp')
Q = Non_terminal('Q', 'ast', 'tmp')


nts = [E, X, T, Y, F, P, M, A, character, W, R, S, B, C, Q]


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

p6 = Production(A, 
               [[character], [openb, E, closedb], [opensb, W, closedsb], [regex_empty], [new_line]],
               [[(A_rule_character_rgx, True)], [(A_rule_brackets_rgx, True)], [(A_rule_square_brackets_rgx, True)],
                [(A_rule_eps_rgx, True)], [(A_rule_new_line, True)]]
               )

p7 = Production(W,
               [[R, S]],
               [[(W_rule_rgx, True), (S1_rule_rgx, False)]]
               )

p8 = Production(S,
               [[R, S], [empty]],
               [[(S2_rule_rgx, False), (S3_rule_rgx, True)], [(S4_rule_rgx, True)]]
               )

p9 = Production(R,
               [[B, Q]],
               [[(Q1_rule_rgx, False), (R1_rule_rgx, True)]]
               )

p10 = Production(Q,
               [[rrange, B, Q], [empty]],
               [[(B1_rule_rgx, False), (Q2_rule_rgx, True)], [(Q3_rule_rgx, True)]]
               )

p11 = Production(B,
               [[character]],
               [[(B_rule_character_rgx, True)]]
               )

p12 = Production(C,
               [[character]],
               [[(C_rule_character_rgx, True)]]
               )

p13 = Production(character,
               [[any_character], [literal, any_character]],
               [[(character_rule_except_metas, True)], [(character_rule_except_specials, True)]]
               )

p14 = Production(P, 
               [[M], [empty]],
               [[(P_rule_M_1_rgx, True), (P_rule_M_2_rgx, False)], [(P_rule_eps_rgx, True)]]
               )

p15 = Production(M, 
               [[clousure], [question], [rplus]],
               [[(M_rule_rgx, True)], [(M_rule_question, True)], [(M_rule_plus, True)]]
               )


prods = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15]

regex_grammar = Grammar(terminals, nts, E, prods)