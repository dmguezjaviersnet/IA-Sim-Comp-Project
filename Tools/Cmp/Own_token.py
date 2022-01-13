from enum import Enum


class Token_Type(Enum):
    # Arth
    character = 1
    plus = 2
    minus = 3
    times = 4
    div = 5

    # Regex
    closure = 6
    union = 7

    repsilon = 11
    open_parenthesis = 8
    closed_parenthesis = 9
    eof = 10


class Token: # Clase para representar los tokens

    def __init__(self, lexem: str, tkn_type: Token_Type): # Ctor
        self.tkn_type = tkn_type
        self.lexem = lexem

    def is_operator(self):
        return self.tkn_type in range(1, 8);
    
    def __str__(self) -> str:
        return f"{self.value} : {self.tkn_type}"
        
        