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
    number = 30

    # Regex
    closure = 6
    union = 7
    repsilon = 10

    eof = 11
    space = 12
    


class Token: # Clase para representar los tokens

    def __init__(self, lexeme: str, token_type: Token_Type): # Ctor
        self.token_type = token_type
        self.lexeme = lexeme

    def is_operator(self):
        return self.token_type.value in range(2, 12)
    
    def __str__(self) -> str:
        return f"{self.lexeme} : {self.token_type}"
        
        