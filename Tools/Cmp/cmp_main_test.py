from Grammar import *
from own_token import *
from nonr_parser import non_recursive_parse
from Terminal import *
from Non_terminal import *
from Production import *
from ll1_table_builder import build_LL1_table
from rules import *

line = input().split()
line.append('$')
tokens = []

#### Lexer para ir probando ####
for i in range(len(line)):
    if line[i] == '+':
        tokens.append(Op('+', Token_Type.plus, 1))

    elif line[i] == '-':
        tokens.append(Op('-', Token_Type.minus, 1))

    elif line[i] == '*':
        tokens.append(Op('*', Token_Type.times, 2))

    elif line[i] == '/':
        tokens.append(Op('/', Token_Type.div, 2))

    elif line[i] == '(':
        tokens.append(Op('(', Token_Type.open_parenthesis, 3))

    elif line[i] == ')':
        tokens.append(Op(')', Token_Type.closed_parenthesis, 3))

    elif line[i] == '$':
        tokens.append(Op('$' ,Token_Type.eof, 1))
    
    else:
        number = 0
        try:
            number = int(line[i])

        except: print('Invalid syntax')
        tokens.append(Num(number, tkn_type=Token_Type.num))

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
integer = Terminal('i')
empty = Terminal('eps')
eof = Terminal('$')
terminals = [add, sub, mul, div, openb, closedb, integer, empty, eof]

# Reglas


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
                [[openb, E, closedb], [integer]],
                [[(F_rule_brackets, True)], [(F_rule_i, True)]]
                )

prods = [p1, p2, p3, p4, p5]



arth_grammar = Grammar(terminals, nts, E, prods,)
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
ast, parsed2 = non_recursive_parse(arth_grammar, tokens)

print(ast)

# print('finished')
# print(parsed2)
# print(parsed)


