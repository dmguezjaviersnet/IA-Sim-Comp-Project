from enum import Enum

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
    
    ########## Simorb

    # átomos
    int = 10
    float = 11
    boolean = 12
    string = 13
    id_orbsim = 31
    
    # binarias
    plus = 14
    minus = 15
    times = 16
    div =  17
    mod = 18

    # unarias
    neg = 19

    # palabras claves
    loop = 20
    func = 21
    if_orbsim = 22
    then = 23
    else_orbsim = 24
    let = 25

    assign = 26

    # agrupamiento
    open_parenthesis = 27
    closed_parenthesis = 28
    open_curly_braces = 29
    closed_curly_braces = 30

    
    eof = 100
    space = 101
    
class Token: # Clase para representar los tokens

    def __init__(self, lexeme: str, token_type: Token_Type): # Ctor
        self.token_type = token_type
        self.lexeme = lexeme

    def is_operator(self):
        return self.token_type.value in range(2, 12)
    
    def __str__(self) -> str:
        return f"{self.lexeme} : {self.token_type}"
        
        