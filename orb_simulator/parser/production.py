from typing import Callable, List, Tuple
from parser.non_terminal import Non_terminal
from parser.own_symbol import Symbol

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
        self.rules = rules

    def __str__(self) -> str:
        ans = f'{self.head.identifier} -> '

        for elem in self.tails[0]:
            ans += f'{elem.__str__()} '

        for tail in self.tails[1:]:
            ans += '\n     '
            for elem in tail:
                ans += f'{elem.__str__()} '

        return ans

