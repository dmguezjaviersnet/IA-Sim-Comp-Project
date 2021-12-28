from typing import overload


class Symbol: # Clase para símbolo de una gramática
    
    '''Representa un símbolo en una gramática, sea terminal o no terminal'''
    
    def __init__(self, id: str, *args): # Ctor
        self.identifier = id
        self.attrs = []

        for elem in args: # Crear campos con los nombres empaquetados en *args
            setattr(self, elem, None)
            self.attrs.append(elem)
            