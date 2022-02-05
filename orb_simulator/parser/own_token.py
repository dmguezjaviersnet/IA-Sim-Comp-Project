from enum import Enum

from numpy import product

class Token_Type(Enum):

    ########## Regex
    character = 1
    closure = 2
    union = 3
    repsilon = 4
    rplus = 5
    question = 6
    rrange = 7
    open_square_brackets = 8
    closed_square_brackets = 9
    literal = 103
    
    ########## Simorb

    # átomos
    int = 10
    float = 11
    boolean = 12
    string = 13
    id_orbsim = 31
    type_id_orbsim = 50
    
    # binarias
    plus = 14
    minus = 15
    mul = 16
    div =  17
    mod = 18

    equals = 32
    not_equals = 40
    less_than = 33
    greater_than = 34
    greater_or_equal_than = 35
    less_or_equal_than = 36
    
    logical_or = 37
    logical_and = 38
    
    bitwise_or = 46
    bitwise_xor = 51
    bitwise_and = 45
    bitwise_not = 47
    bitwise_shift_left = 48
    bitwise_shift_right = 49

    # unarias
    neg = 19

    # palabras claves
    let = 25
    func = 21
    class_orbsim = 52
    if_orbsim = 22
    then = 23
    else_orbsim = 24
    loop = 20
    return_orbsim = 39
    make_orbsim = 41
    continue_orbsim = 42
    break_orbsim = 43
    print_orbsim = 44

    assign = 26

    # agrupamiento
    open_parenthesis = 27
    closed_parenthesis = 28
    open_curly_braces = 29
    closed_curly_braces = 30

    
    eof = 100
    space = 101
    new_line = 102
    stmt_separator = 104
    expr_separator = 105
    error = 106
    
class Token: # Clase para representar los tokens

    def __init__(self, lexeme: str, token_type: Token_Type): # Ctor
        self.token_type = token_type
        self.lexeme = lexeme

    def is_operator(self):
        return self.token_type.value in range(2, 12)
    
    def __str__(self) -> str:
        return f"{self.lexeme} : {self.token_type}"
        
        