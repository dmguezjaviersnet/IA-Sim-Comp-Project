# Aquí iremos probando las herramientas de Compilación
from own_token import *
from grammar import Grammar
from nonr_parser import non_recursive_parse

line = input().split()
line.append('$')
tokens = []

#### Lexer para ir probando ####
for i in range(len(line)):
    if line[i] == '+':
        tokens.append(Symbol('+', Token_Type.plus, 1))

    elif line[i] == '-':
        tokens.append(Symbol('-', Token_Type.minus, 1))

    elif line[i] == '*':
        tokens.append(Symbol('*', Token_Type.times, 2))

    elif line[i] == '/':
        tokens.append(Symbol('/', Token_Type.div, 2))

    elif line[i] == '(':
        tokens.append(Symbol('(', Token_Type.open_parenthesis, 3))

    elif line[i] == ')':
        tokens.append(Symbol(')', Token_Type.closed_parenthesis, 3))

    elif line[i] == '$':
        tokens.append(Symbol('$' ,Token_Type.eof, 1))
    
    else:
        number = 0
        try:
            number = int(line[i])

        except: print('Invalid syntax')
        tokens.append(Number(number, tkn_type=Token_Type.num))


terminals = ['+', '-', '*', '/', '(', ')', 'integer', 'epsilon', '$']
non_terminals = ['E', 'X', 'T', 'Y', 'F']
initial_nt = 'E'
prod = {
    'E': [['T', 'X']], 
    'X': [['+', 'E'], ['-', 'E'], ['epsilon']],
    'T': [['F', 'Y']],
    'Y': [['*', 'T'], ['/', 'T'], ['epsilon']],
    'F': [['(', 'E', ')'], ['integer']]
 }

arth_grammar = Grammar(terminals, non_terminals, initial_nt, prod)
# is_ll1, table = build_LL1_table(arth_grammar) 
# 
# for ter, dict1 in table.items():
    # print(f'\'{ter}\' column -------------------------- //')
    # for nt, prod in dict1.items():
        # print(f'{nt} row -----> {prod}')
parsed = non_recursive_parse(arth_grammar, tokens)

print(f'Parsing finished !!!!!')

if parsed:
    print('Valid sentence !!!!!!')
else : 
    print('Invalid sentence')

# print(parsed)
