from typing import Dict
from Grammar import *
from Own_token import *
from nonr_parser import non_recursive_parse
from Terminal import *
from Non_terminal import *
from Production import *

from rules import *
from regex_rules import *


# arth_token_builder: Dict[str, Callable] = {
#     '+': lambda : tokens.append(Op('+', Token_Type.plus, 1)),
#     '-': lambda : tokens.append(Op('-', Token_Type.minus, 1)),
#     '*': lambda : tokens.append(Op('*', Token_Type.times, 2)),
#     '/': lambda : tokens.append(Op('/', Token_Type.div, 2)),
#     '(': lambda : tokens.append(Op('(', Token_Type.open_parenthesis, 3)),
#     ')': lambda : tokens.append(Op(')', Token_Type.closed_parenthesis, 3)),
#     '$': lambda : tokens.append(Op('$' ,Token_Type.eof, 1))
# }

regex_token_builder: Dict[str, Callable] = {
    '*': Op('*', Token_Type.closure, 3),
    '(': Op('(', Token_Type.open_parenthesis, 3),
    ')': Op(')', Token_Type.closed_parenthesis, 3),
    '|': Op('|', Token_Type.union, 1),
    'ε': Op('ε', Token_Type.repsilon, 2),
    '$': Op('$' ,Token_Type.eof, 1)
}

# arth_line = input().split()
# arth_line.append('$')

# #### Lexer para ir probando ####
# for i in range(len(arth_line)):
#     if arth_line[i] in arth_token_builder.keys():
#         arth_token_builder[arth_line[i]]()
    
#     else:
#         number = 0
#         try:
#             number = int(arth_line[i])

#         except: print('Invalid syntax')
#         tokens.append(Character(number, tkn_type=Token_Type.character))

############################### Gramática de prueba (aritmética) ###########################################

# No terminales
E = Non_terminal('E', 'ast')
X = Non_terminal('X', 'ast', 'tmp')
T = Non_terminal('T', 'ast', 'tmp')
Y = Non_terminal('Y', 'ast', 'tmp')
F = Non_terminal('F', 'ast')
nts = [E, X, T, Y, F]

# Terminales
mul = Terminal('*')
div = Terminal('/')
add = Terminal('+')
sub = Terminal('-')
openb = Terminal('(')
closedb = Terminal(')')
character = Terminal('character')
empty = Terminal('eps')
eof = Terminal('$')
terminals = [add, sub, mul, div, openb, closedb, character, empty, eof]

# Producciones
p1 = Production(E, 
                [[T, X]],
                [[(E_rule, True), (X_rule, False)]]
                )

p2 = Production(X, 
                [[add, T, X], [sub, T, X], [empty]],
                [[(X0_rule_plus, True), (X1_rule_plus, False)], [(X0_rule_minus, True), (X1_rule_minus, False)], [(X0_rule_eps, True)]]
                )

p3 = Production(T, 
                [[F, Y]], 
                [[(T_rule, True), (Y_rule, False)]]
                )

p4 = Production(Y, 
                [[mul, F, Y], [div, F, Y], [empty]], 
                [[(Y0_rule_mul, True), (Y1_rule_mul, False)], [(Y0_rule_div, True), (Y1_rule_div, False)], [(Y0_rule_eps, True)]]
                )

p5 = Production(F, 
                [[openb, E, closedb], [character]],
                [[(F_rule_brackets, True)], [(F_rule_i, True)]]
                )

prods = [p1, p2, p3, p4, p5]

arth_grammar = Grammar(terminals, nts, E, prods)
# terminals = ['+', '-', '*', '/', '(', ')', 'integer', 'epsilon', '$']
# non_terminals = ['E', 'X', 'T', 'Y', 'F']
# initial_nt = 'E'
# prod = {
#     'E': [['T', 'X']], 
#     'X': [['+', 'E'], ['-', 'E'], ['epsilon']],
#     'T': [['F', 'Y']],
#     'Y': [['*', 'T'], ['/', 'T'], ['epsilon']],
#     'F': [['(', 'E', ')'], ['integer']]
#  }

# parser = Arth_RecDesc_Parser(tokens)
# parsed1 = parser.Parse()

# arth_grammar = Grammar(terminals, non_terminals, initial_nt, prod)
# is_ll1, table = build_LL1_table(arth_grammar)
# 
# for ter, dict1 in table.items():
    # print(f'\'{ter}\' column -------------------------- //')
    # for nt, prod in dict1.items():
        # print(f'{nt} row -----> {prod}')
        
# ast, parsed2 = non_recursive_parse(arth_grammar, tokens)
# print(ast)

############################### Gramática de Regex #################################

# tokens.clear()
# regex_line = input().split()
# regex_line.append('$')


def regexTokenizer(regex_line: str):
    tokens = []
    line = regex_line.split()
    line.append('$')

    for token in line:
        for symbol in token:
            if symbol in regex_token_builder:
                tokens.append(regex_token_builder[symbol])
    
            else:
                tokens.append(Character(symbol, tkn_type=Token_Type.character))
    
    return tokens

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

tokens = regexTokenizer('(a|ε)*')
ast, parsed2 = non_recursive_parse(regex_grammar, tokens)
# print(parsed2)
nfa = ast.eval()
dfa = NFAtoDFA(nfa)
print(dfa.match('aaaaa'))
print(dfa.match('abbbbed'))
print(dfa.match('aaed'))
print(dfa.match('ed'))
print(dfa.match('aaaaabbbbaaed'))
print(dfa.match('aaaaabbbba'))
print(dfa.match(''))

print('finished')
# print(parsed2)
# print(parsed)


