from typing import Dict, List, Set, Tuple
from parser.own_symbol import Symbol
from parser.grammar import Grammar

def __belongs (lit: str, prod: List[Symbol]) -> bool:
    for elem in prod:
        if elem.identifier == lit:
            return True
    return False

def find_firsts(G: Grammar) -> Dict[str, Set]: # Para calcular los Firsts de cada no-terminal
    firsts: dict[str, Set] = {}
    for ter in G.terminals: # Calculando los First de cada terminal
        firsts[ter.identifier] = set() # Inicializando los sets de los Firsts de los terminales
        firsts[ter.identifier].add(ter.identifier) # Cada terminal está en su propio First

    for noter in G.non_terminals: # Por cada no-terminal
        firsts[noter.identifier] = set() # Inicializando los sets para almacenar sus Firsts

    changed = True

    while changed: # Mientras cambie algún First 
        changed = False
        for coll in G.productions: # Por cada collección de no-terminal y su correspondiente lista de producciones
            head = coll.head
            for prod in coll.tails: # Por cada producción X -> W
                if __belongs('eps', prod): # Si es X -> epsilon
                    contains = True if 'eps' in firsts[head.identifier] else False
                    if not contains: # Si no contiene epsilon en el First
                        firsts[head.identifier].add('eps') # Lo añadimos
                        changed = True # Indicamos que cambió un First para indicar que hay que volver a analizar las producciones.

                else: ### Si es X -> W : W != epsilon
                    all_eps = True # Asumimos inicialmente que todos los elementos de la forma oracional W pueden irse a epsilon
                    for elem in prod: # Por cada producción
                        contains = True if firsts[elem.identifier].issubset(firsts[head.identifier]) else False
                        if not contains: # Si el First de elem no está en First(X)
                            firsts[head.identifier] = firsts[head.identifier].union(firsts[elem.identifier]) # Lo añadimos
                            changed = True # Indicamos que cambió un First para indicar que hay que volver a analizar las producciones.

                        if 'eps' not in firsts[elem.identifier]: # Si eps no estaba en el First de elem
                            all_eps = False # Entonces este elem no se va a epsilon y por tanto el First(X) se reduce a los Firsts computados hasta este elem
                            break # Paramos porque ya no hay más Firsts que computar en esta producción
                    
                    if all_eps: # Si nada cambió, es porque en efecto todos los elementos de la forma oracional W se fueron a epsilon 
                        contains = True if 'eps' in firsts[head.identifier] else False
                        if not contains: # Por si epsilon no estaba en el First(X)
                            firsts[head.identifier].add('eps') # Lo añadimos
                            changed = True # Indicamos que cambió un First para indicar que hay que volver a analizar las producciones
    return firsts
        
def find_first (symbols: List[Symbol], firsts: Dict[str, Set]) -> Set[str]: ### Para calcular el first de cualquier forma oracional
    result: Set[str] = set()
    all_eps = True
    for elem in symbols:
        result = result.union(firsts[elem.identifier])
        if 'eps' not in firsts[elem.identifier]:
            all_eps = False
            break
    
    if all_eps:
        result.add('eps')
    
    return result

def __find_follows(G, firsts) -> Dict[str, Set]: # Para calcular los Follows
    follows: dict[str, Set] = {} # Inicializamos el diccionario donde vamos a almacenar los sets que contienen los Follows de cada no-terminal

    for nt in G.non_terminals:
        follows[nt.identifier] = set() # Inicializamos cada uno de los sets de cada no-terminal

    follows[G.initial_nt.identifier].add('$') # $ está en el Follow(X) para todo X.

    changed = True
    while changed: # Mientras cambie algún Follow
        changed = False
        for coll in G.productions: # Por cada collección de no-terminal y su correspondiente lista de producciones
            head: Symbol = coll.head  # Almacenamos la el no-terminal
            for prod in coll.tails: # Por cada producción X -> W
                for i, elem in enumerate(prod): # Por cada símbolo en la parte derecha de la producción

                    if elem in G.terminals: # Si es un terminal
                        continue # Simplemente pasamos a analizar el próximo elemento de la forma oracional W

                    first1: Set[str] = find_first(prod[i+1::], firsts) # Computamos el first de la forma oracional W, a partir del elemento detrás del actual
                    first2 = first1.copy() # Creamos una copia que nos va a hacer falta luego
                    
                    if 'eps' in first1: # Si eps esta en el First(Z) donde Z es la forma oracional que viene detrás de elem
                        first1.remove('eps') # Lo quitamos del First(Z)

                    contains_all1 = True if first1.issubset(follows[elem.identifier]) else False
                    if not contains_all1: # Si el First(Z) no está en el Follow(elem)
                        follows[elem.identifier] = follows[elem.identifier].union(first1) # Lo añadimos
                        changed = True # Indicamos que cambió un Follow para indicar que hay que volver a analizar las producciones
                    
                    if 'eps' in first2 or i == len(prod) - 1: # Si eps estuvo en el First(Z) [para eso usamos la copia], o estamos en el último elem de W 
                        contains_all2 = True if follows[head.identifier].issubset(follows[elem.identifier]) else False
                        if not contains_all2: # Si el Follow(X) no está en el Follow(elem)
                            follows[elem.identifier] = follows[elem.identifier].union(follows[head.identifier]) # Lo añadimos
                            changed = True # Indicamos que cambió un Follow para indicar que hay que volver a analizar las producciones
    return follows

def build_LL1_table(G: Grammar) -> Tuple[bool, Dict[str, Dict[str, List[str]]]]: ### Intenta construir la tabla LL (la salida depende de si la grámatica es LL(1))
    
    table: dict[str, dict[str, list[str]]] = {} # Inicializando tabla LL
    firsts: dict[str, Set] = find_firsts(G) # Computando Firsts
    follows: dict[str, Set] = __find_follows(G, firsts) # Computando Follows

    for coll in G.productions: # Por cada collección de no-terminal y su correspondiente lista de producciones
        head: Symbol = coll.head # Almacenamos el no-terminal
        for prod in coll.tails: # Por cada producción X -> W
            current_first = find_first(prod, firsts) # Computamos el First(W)
            for ter in G.terminals: # Por cada posible token (terminales)
                if ter.identifier != 'eps': # Ignorar eps en la Tabla, no se pone
                    if ter.identifier not in table: # Si aún no hay ningún token t con este identificador en la tabla
                        table[ter.identifier] = {} # Inicializar un Dict para él
    
                    if head.identifier not in table[ter.identifier]: # Si aún no hay ningún no-terminal con este identificador en la tabla
                            table[ter.identifier][head.identifier] = [] # Inicializar una lista para guardar la producción correspondiente a este par [X, t]
    
                    if 'eps' in prod[0].identifier and ter.identifier in follows[head.identifier] or ter.identifier in current_first: # Si t está en el First(X) o t está en el Follow(X) y W = eps => [X, t] = W
                        if len(table[ter.identifier][head.identifier]) == 0: # Si la tabla en esa posición está vacía
                            table[ter.identifier][head.identifier] = prod # Almacenar la producción
                        
                        else : return False, None # Si no esta vacía la tabla en esa posición entonces la gramática no es LL(1)
    return True, table