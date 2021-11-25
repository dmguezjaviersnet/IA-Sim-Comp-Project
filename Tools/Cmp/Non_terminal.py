from typing import overload
from Own_symbol import Symbol


class Non_terminal(Symbol):
    
    def __init__(self, identifier: str, *args):
        super().__init__(identifier, *args)