from enum import Enum


class Token_Type(Enum):
    # Arth
    character = 1
    plus = 2
    minus = 3
    times = 4
    div = 5
    open_parenthesis = 6
    closed_parenthesis = 7
    number = 8

    # Regex
    closure = 9
    union = 10
    repsilon = 11
    rplus = 12
    question = 13
    rrange = 14
    open_square_brackets = 15
    closed_square_brackets = 16

    eof = 17
    space = 18
    


class Token: # Clase para representar los tokens

    def __init__(self, lexeme: str, token_type: Token_Type): # Ctor
        self.token_type = token_type
        self.lexeme = lexeme

    def is_operator(self):
        return self.token_type.value in range(2, 12)
    
    def __str__(self) -> str:
        return f"{self.lexeme} : {self.token_type}"
        
        