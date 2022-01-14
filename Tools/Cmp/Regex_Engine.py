from typing import Callable, Dict
from Own_token import Token, Token_Type
from automaton import *
from nonr_parser import non_recursive_parse
from regex_grammar import *


regex_token_builder: Dict[str, Callable] = {
    '*': Token('*', Token_Type.closure),
    '(': Token('(', Token_Type.open_parenthesis),
    ')': Token(')', Token_Type.closed_parenthesis),
    '|': Token('|', Token_Type.union),
    'ε': Token('ε', Token_Type.repsilon),
}

class Regex_Engine:

    def __init__(self, regex: str):
        self.regex = regex
        self.automaton: 'Automaton' = self._build_automaton()

    

    
    def _build_automaton(self) -> 'Automaton':
        tokens = self._regexTokenizer()
        _, ast = non_recursive_parse(regex_grammar, tokens)
        nfa = ast.eval()        
        return nfa


    def _regexTokenizer(self) -> List[Token]:
        tokens = []

        literal = False

        for symbol in self.regex:
            if literal:
                tokens.append(Token(symbol, token_type=Token_Type.character)) 
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
                    tokens.append(Token(symbol, token_type=Token_Type.character))
        tokens.append(Token('$' ,Token_Type.eof))
        return tokens

