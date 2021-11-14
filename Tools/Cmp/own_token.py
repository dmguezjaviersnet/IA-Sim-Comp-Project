from enum import Enum


class Token_Type(Enum):
    num = 1
    plus = 2
    minus = 3
    times = 4
    div = 5
    open_parenthesis = 6
    closed_parenthesis = 7
    eof = 8

class Token:

    def __init__(self, value, tkn_type):
        self.tkn_type = tkn_type
        self.value = value

class Number(Token):

    def __init__(self, value, tkn_type):
        super().__init__(value, tkn_type)

class Op(Token):

    def __init__(self, value, tkn_type, priority):
        super().__init__(value, tkn_type)
        self.priority = priority
        
        