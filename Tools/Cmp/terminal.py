from typing import overload
from own_symbol import Symbol

class Terminal(Symbol): # Clase para terminal de una gramática
    
    '''Clase que representa un nodo de un terminal de una gramática, en el árbol de derivación'''

    def __init__(self, identifier: str, *args): # Ctor
        super().__init__(identifier, *args)

class Eof(Terminal): # Caracter especial $

    def __init__(self, *args):
        super().__init__('$', *args)

class Epsilon(Terminal): # Caracter especial que indica producción epsilon 

    def __init__(self, *args):
        super().__init__('eps', *args)