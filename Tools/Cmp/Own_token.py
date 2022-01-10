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

    def __init__(self, value, tkn_type): # Ctor
        self.tkn_type = tkn_type
        self.value = value
    
    def __str__(self) -> str:
        return f"{self.value}:{self.tkn_type}"

class Character(Token): # Clase para representar los caracteres

    def __init__(self, value, tkn_type): # Ctor
        super().__init__(value, tkn_type)

class Op(Token): # Clase para representar los Operadores

    def __init__(self, value, tkn_type, priority): # Ctor
        super().__init__(value, tkn_type)
        self.priority = priority
        
        