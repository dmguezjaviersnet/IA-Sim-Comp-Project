from typing import Callable, Dict
from Own_token import Token, Token_Type
from Grammar import Grammar
from Non_terminal import Non_terminal
from Production import Production
from Terminal import Terminal, Epsilon, Eof
from arth_grammar_rules import *

'''
    Gramática aritmética básica LL(1)
    E -> T X
    X -> + T X
        | - T X
        | epsilon
    T -> F Y
    Y -> * F Y
        | / F Y 
        | epsilon
    F -> ( E )
        | int

    Gramática aritmética básica
    E -> T + E
        | T - E
        | T
    T -> F * T 
        | F / T
        | F
    F -> ( E )
        | character

'''

arth_token_builder: Dict[str, Callable] = {
    '+': lambda : Token('+', Token_Type.plus),
    '-': lambda : Token('-', Token_Type.minus),
    '*': lambda : Token('*', Token_Type.times),
    '/': lambda : Token('/', Token_Type.div),
    '(': lambda : Token('(', Token_Type.open_parenthesis),
    ')': lambda : Token(')', Token_Type.closed_parenthesis),
    '$': lambda : Token('$' ,Token_Type.eof)
}

def arth_grammar_tokenize(line: str) -> List[Token]:
    line += '$'

    tokens: List[Token] = []
    #### Lexer para ir probando ####
    for i in range(len(line)):
        if line[i] in arth_token_builder.keys():
            tokens.append(arth_token_builder[line[i]]())
      
        else:
            number = 0
            try:
                number = int(line[i])
            except: print('Invalid syntax')
            tokens.append(Token(number, Token_Type.int))

    return tokens

# No terminales

E = Non_terminal('E', 'ast')
T = Non_terminal('T', 'ast', 'tmp')
F = Non_terminal('F', 'ast')
nts = [E, T, F]

# Terminales
mul = Terminal('*')
div = Terminal('/')
add = Terminal('+')
sub = Terminal('-')
openb = Terminal('(')
closedb = Terminal(')')
int = Terminal('int')
empty = Epsilon()
eof = Eof()
terminals = [add, sub, mul, div, openb, closedb, int, empty, eof]

# Producciones
p1 = Production(E,
                [[T, add, E], [T, sub, E], [T]],
                [[(E1_rule, True)], [(E2_rule, True)], [(E3_rule, True)]]
                )

p2 = Production(T, 
                [[F, mul, T], [F, div, T], [F]], 
                [[(T1_rule, True)], [(T2_rule, True)], [(T3_rule, True)]]
                )

p3 = Production(F, 
                [[openb, E, closedb], [int]],
                [[(F1_rule, True)], [(F2_rule, True)]]
                )
prods = [p1, p2, p3]

arth_grammar = Grammar(terminals, nts, E, prods)

arth_grammar_token_string = {
    Token_Type.int: 'int',
    Token_Type.plus : '+',
    Token_Type.minus : '-',
    Token_Type.times : '*',
    Token_Type.div : '/',
    Token_Type.open_parenthesis : '(',
    Token_Type.closed_parenthesis : ')',
    Token_Type.eof : '$'
}