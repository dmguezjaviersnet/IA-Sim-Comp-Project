from grammar import *
from own_token import *
from nonr_parser import non_recursive_parse
from terminal import *
from non_terminal import *
from production import *
from ll1_table_builder import build_LL1_table


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
        tokens.append(Number(number, tkn_type=Token_Type.num))

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
p1 = Production(E, [[T, X]])
p2 = Production(X, [[add, T, X], [sub, T, X], [empty]])
p3 = Production(T, [[F, Y]])
p4 = Production(Y, [[mul, F, Y], [div, F, Y], [empty]])
p5 = Production(F, [[openb, E, closedb], [integer]])

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
is_ll1, table = build_LL1_table(arth_grammar)
# 
# for ter, dict1 in table.items():
    # print(f'\'{ter}\' column -------------------------- //')
    # for nt, prod in dict1.items():
        # print(f'{nt} row -----> {prod}')
parsed2 = non_recursive_parse(arth_grammar, tokens)

# print('finished')
# print(parsed2)
# print(parsed)


