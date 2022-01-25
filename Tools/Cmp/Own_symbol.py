class Symbol: # Clase para símbolo de una gramática
    
    '''Representa un símbolo en una gramática, sea terminal o no terminal'''
    
    def __init__(self, id: str, *args): # Ctor
        self.identifier = id
        self.attrs = []

        for elem in args: # Crear campos con los nombres empaquetados en *args
            setattr(self, elem, None)
            self.attrs.append(elem)

    def __str__(self) -> str:
        return self.identifier

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Symbol):
            return self.identifier == __o.identifier

        return False
    
    def __hash__(self) -> int:
        return hash(self.identifier)
            