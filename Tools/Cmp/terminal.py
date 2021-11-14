from typing import overload
from own_symbol import Symbol


class Terminal(Symbol):

    def __init__(self, identifier: str, *args):  # Falta agregarle las propiedades fila y columna
        super().__init__(identifier, *args)