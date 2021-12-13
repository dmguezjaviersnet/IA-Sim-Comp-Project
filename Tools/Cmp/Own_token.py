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


class Token:

    def __init__(self, value, tkn_type):
        self.tkn_type = tkn_type
        self.value = value

class Character(Token):

    def __init__(self, value, tkn_type):
        super().__init__(value, tkn_type)

class Op(Token):

    def __init__(self, value, tkn_type, priority):
        super().__init__(value, tkn_type)
        self.priority = priority
        
        