from typing import overload
from Own_symbol import Symbol


class Non_terminal(Symbol): # Clase para terminal de una gramática
    
    def __init__(self, identifier: str, *args): # Ctor
        super().__init__(identifier, *args)
