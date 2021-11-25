from typing import overload
from Own_symbol import Symbol


class Terminal(Symbol):

    def __init__(self, identifier: str, *args):
        super().__init__(identifier, *args)

class EOF(Terminal):

    def __init__(self, identifier: str, *args):
        super().__init__('$',*args)

class Epsilon(Terminal):

    def __init__(self, identifier: str, *args):
        super().__init__('epsilon', *args)