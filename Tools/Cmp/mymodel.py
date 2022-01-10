class Token:
    """
    Token Class

    
    """

    def __init__(self, lexeme, token_type):
        self.lexeme = lexeme
        self.token_type = token_type
    
    def __str__(self):
        return f'{self.token_type}: {self.lexeme}'
    
    def __repr__(self) -> str:
        return str(self)
    