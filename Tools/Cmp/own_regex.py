from typing import Callable, Dict
from Own_token import Character, Op, Token_Type
from automaton import *
from nonr_parser import non_recursive_parse
from regex_grammar import *

import mymodel

regex_token_builder: Dict[str, Callable] = {
    '*': Op('*', Token_Type.closure, 3),
    '(': Op('(', Token_Type.open_parenthesis, 3),
    ')': Op(')', Token_Type.closed_parenthesis, 3),
    '|': Op('|', Token_Type.union, 1),
    'ε': Op('ε', Token_Type.repsilon, 2),
    '$': Op('$' ,Token_Type.eof, 1)
}
class Regex:

    def __init__(self, regex):
        self.regex = regex
        self.automaton: 'DFA' = self.build_automaton(regex)

    def __call__(self, text):
        return self.automaton.match(text)

    @staticmethod
    def build_automaton(regex)-> DFA:
        tokens = regexTokenizer(regex)
        ast, _ = non_recursive_parse(regex_grammar, tokens)
        nfa = ast.eval()
        
        return nfa


def regexTokenizer(regex_text: str):
    tokens = []
    
    literal = False

    for symbol in regex_text:
        if literal:
            tokens.append(Character(symbol, tkn_type=Token_Type.character)) 
            literal = False
            
        elif symbol.isspace():
            continue   
        
        elif symbol =='\\':
            literal =  True
            continue  
        
        else:
            if symbol in regex_token_builder.keys():
                tokens.append(regex_token_builder[symbol])
    
            else:
                tokens.append(Character(symbol, tkn_type=Token_Type.character))
    
    return tokens

def main():
   regex = Regex('(a|b)*')
   print(regex.automaton)


main()

