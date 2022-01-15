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
    '''
        Clase que representa el motor de expresiones regulares
        Crea el autómata para reconocer cadenas que matchean con la 
        expresión regular con la que se inicilizó la clase
    '''
    def __init__(self, regex: str):
        self.regex = regex
        self.automaton: 'Automaton' = self._build_automaton()

    

    
    def _build_automaton(self) -> 'Automaton':
        tokens = Regex_Engine.regexTokenizer(self.regex)
        _, ast = non_recursive_parse(regex_grammar, tokens)
        nfa = ast.eval()        
        return nfa

    @staticmethod
    def regexTokenizer(text) -> List[Token]:
        '''
            Dado una cadena de entrada (que seríá una expresión regular) devuelve los tokens necesarios 
            para ser usado en el parser LL(1) que parsearíá dicha expresión regular.
        '''
        tokens = []

        literal = False

        for symbol in text: # va por cada carácter de la cadena
            if literal: # si es un carácter literal
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

