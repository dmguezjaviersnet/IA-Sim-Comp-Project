from typing import Callable, Dict
from own_token import Token, Token_Type
from grammar import Grammar
from non_terminal import Non_terminal
from terminal import Terminal, Epsilon, Eof
from production import Production
from arth_grammar_rules import *


lr1_test_token_builder: Dict[str, Callable] = {
    '+': lambda : Token('+', Token_Type.plus),
    '=': lambda : Token('=', Token_Type.assign),
    '$': lambda : Token('$' ,Token_Type.eof)
}

def test_grammar_tokenize(line: str) -> List[Token]:
    line += '$'

    tokens: List[Token] = []
    #### Lexer para ir probando ####
    for i in range(len(line)):
        if line[i] in lr1_test_token_builder:
            tokens.append(lr1_test_token_builder[line[i]]())

        else:
            number = 0
            try:
                number = int(line[i])
            except: print('Invalid syntax')
            tokens.append(Token(number, Token_Type.character))

    return tokens

# No terminales

E = Non_terminal('E', 'ast')
A = Non_terminal('A', 'ast', 'tmp')

nts = [E, A]

# Terminales
assign = Terminal('=')
plus = Terminal('+')
character = Terminal('character')
empty = Epsilon()
eof = Eof()
terminals = [assign, plus, character, empty, eof]

# Producciones
p1 = Production(E,
                [[A, assign, A], [character]],
                [[(E1_rule, True)], [(E2_rule, False)]]
                )

p2 = Production(A, 
                [[character, plus, A], [character]],
                [[(E3_rule, True), (T1_rule, False)], [(T2_rule, True), (T3_rule, False)]]
                )

prods = [p1, p2]

lr1_test_grammar = Grammar(terminals, nts, E, prods)