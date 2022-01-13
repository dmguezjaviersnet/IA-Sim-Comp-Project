from enum import Enum


class Token_Type(Enum):
    # Arth
    character = 1
    plus = 2
    minus = 3
    times = 4
    div = 5
    open_parenthesis = 8
    closed_parenthesis = 9

    # Regex
    closure = 6
    union = 7
    repsilon = 10

    eof = 11


class Token: # Clase para representar los tokens

    def __init__(self, lexeme: str, token_type: Token_Type): # Ctor
        self.tkn_type = token_type
        self.lexeme = lexeme

    def is_operator(self):
        return self.tkn_type.value in range(2, 11);
    
    def __str__(self) -> str:
        return f"{self.value} : {self.tkn_type}"
        
        