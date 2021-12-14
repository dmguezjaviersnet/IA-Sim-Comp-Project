from typing import Callable, List, Tuple
from Non_terminal import *
from Own_symbol import Symbol

class Production: # Clase para representar una producción
    '''
        Para nosotros una producción será algo de la forma:
    
        Y -> X1 | X2 | ... | Xn

        y por tanto representaremos esta idea usando una 'cabeza' de producción que sería el no-terminal que está a la izquierda de la
        ->, y el resto lo representaremos como una lista de listas de Symbol (la clase que definimos para representar terminales y no terminales)
        , donde estará almacenada cada una de las 'colas', o formas oracionales que resulten de aplicar cada una de las producciones de este no-terminal 
        'cabeza'.
    '''
    def __init__(self, head: Non_terminal, tails: List[List[Symbol]], rules: List[List[Tuple[Callable, bool]]]): # Ctor
        self.head = head
        self.tails = tails
        
        self.nt_in_prod = [0 for i in range(len(self.tails))]
        self.__map_nt_amount()

        self.rules = rules

    
    def __map_nt_amount(self):
        for i in range(len(self.tails)):
            nt_count = 0
            for elem in self.tails[i]:
                if isinstance(elem, Non_terminal):
                    nt_count += 1
            self.nt_in_prod[i] = nt_count

