from typing import Callable, Dict
from Own_token import Character, Op, Token, Token_Type
from Grammar import Grammar
from Non_terminal import Non_terminal
from Production import Production
from Terminal import *
from rules import *


arth_token_builder: Dict[str, Callable] = {
    '+': lambda : Op('+', Token_Type.plus, 1),
    '-': lambda : Op('-', Token_Type.minus, 1),
    '*': lambda : Op('*', Token_Type.times, 2),
    '/': lambda : Op('/', Token_Type.div, 2),
    '(': lambda : Op('(', Token_Type.open_parenthesis, 3),
    ')': lambda : Op(')', Token_Type.closed_parenthesis, 3),
    '$': lambda : Op('$' ,Token_Type.eof, 1)
}

def arth_grammar_tokenize() -> List[Token]:
    arth_line = input().split()
    arth_line.append('$')

    tokens: List[Token] = []
    #### Lexer para ir probando ####
    for i in range(len(arth_line)):
        if arth_line[i] in arth_token_builder.keys():
            arth_token_builder[arth_line[i]]()
      
        else:
            number = 0
            try:
                number = int(arth_line[i])
            except: print('Invalid syntax')
            tokens.append(Character(number, tkn_type=Token_Type.character))

    return tokens

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
empty = Epsilon()
eof = EOF()
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