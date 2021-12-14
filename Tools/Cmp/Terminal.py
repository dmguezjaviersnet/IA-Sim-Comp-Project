from typing import overload
from Own_symbol import Symbol


class Terminal(Symbol): # Clase para terminal de una gramática

    def __init__(self, identifier: str, *args): # Ctor
        super().__init__(identifier, *args)

class EOF(Terminal): # Caracter especial $

    def __init__(self, identifier: str, *args):
        super().__init__('$', *args)

class Epsilon(Terminal): # Caracter especial que indica producción epsilon 

    def __init__(self, identifier: str, *args):
        super().__init__('epsilon', *args)