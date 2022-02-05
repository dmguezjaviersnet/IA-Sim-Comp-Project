from typing import overload
from parser.own_symbol import Symbol


class Non_terminal(Symbol): # Clase para terminal de una gramática

    '''Clase que representa un nodo de un no-terminal de una gramática, en el árbol de derivación'''
    
    def __init__(self, identifier: str, *args): # Ctor
        super().__init__(identifier, *args)
