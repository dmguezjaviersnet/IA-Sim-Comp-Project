from Own_symbol import Symbol
from Grammar import Grammar
from Own_token import Op


def __belongs (lit: str, prod: list[Symbol]) -> bool:
    for elem in prod:
        if elem.identifier == lit:
            return True
    return False

def __find_firsts(G: Grammar) -> dict[str, set]: ### Para calcular los firsts de cada no-terminal
    firsts: dict[str, set] = {}
    for ter in G.terminals: ### Calculando los first de cada terminal
        firsts[ter.identifier] = set()
        firsts[ter.identifier].add(ter.identifier)

    for noter in G.non_terminals:
        firsts[noter.identifier] = set() ### Inicializando los sets para almacenar los firsts de los no terminales

    changed = True

    while changed: ### Mientras cambie algún first 
        changed = False
        for coll in G.productions: ### Por cada collección de no-terminal y su correspondiente lista de producciones
            head = coll.head
            for prod in coll.tails: ### Por cada producción X -> W
                if __belongs('eps', prod): ### Si es X -> epsilon
                    contains = True if 'eps' in firsts[head.identifier] else False
                    if not contains: 
                        firsts[head.identifier].add('eps')
                        changed = True

                else: ### Si es X -> W : W != epsilon
                    all_eps = True
                    for elem in prod:
                        contains = True if firsts[elem.identifier].issubset(firsts[head.identifier]) else False
                        if not contains:
                            firsts[head.identifier] = firsts[head.identifier].union(firsts[elem.identifier])
                            changed = True

                        if 'eps' not in firsts[elem.identifier]:
                            all_eps = False
                            break
                    
                    if all_eps:
                        contains = True if 'eps' in firsts[head.identifier] else False
                        if not contains:
                            firsts[head.identifier].add('eps')
                            changed = True
    return firsts
        
def __find_first (symbols: list[Symbol], firsts: list[str]) -> set[str]: ### Para calcular el first de cualquier forma oracional
    result = set()
    all_eps = True
    for elem in symbols:
        result = result.union(firsts[elem.identifier])
        if 'eps' not in firsts[elem.identifier]:
            all_eps = False
            break
    
    if all_eps:
        result.add('eps')
    
    return result

def __find_follows(G, firsts) -> dict[str, set]: ### Para calcular los follow
    follows: dict[str, set] = {}

    for nt in G.non_terminals:
        follows[nt.identifier] = set()

    follows[G.initial_nt.identifier].add('$')

    changed = True
    while changed:
        changed = False
        for coll in G.productions: ### Por cada collección de no-terminal y su correspondiente lista de producciones
            head: Symbol = coll.head 
            for prod in coll.tails: ### Por cada producción X -> W
                for i in range(len(prod)): ### Por cada símbolo en la parte derecha de la producción
                    temp: Symbol = prod[i]

                    if temp in G.terminals: ### Si es un terminal
                        continue

                    first1: set[str] = __find_first(prod[i+1::], firsts)
                    first2 = first1.copy()
                    
                    if 'eps' in first1:
                        first1.remove('eps')

                    contains_all1 = True if first1.issubset(follows[temp.identifier]) else False
                    if not contains_all1:
                        follows[temp.identifier] = follows[temp.identifier].union(first1)
                        changed = True
                    
                    if 'eps' in first2 or i == len(prod) - 1:
                        contains_all2 = True if follows[head.identifier].issubset(follows[temp.identifier]) else False
                        if not contains_all2:
                            follows[temp.identifier] = follows[temp.identifier].union(follows[head.identifier])
                            changed = True
    return follows

def build_LL1_table(G: Grammar) -> tuple[bool, dict[str, dict[str, list[str]]]]: ### Intenta construir la tabla LL (la salida depende de si la grámatica es LL(1))
    
    table: dict[str, dict[str, list[str]]] = {}
    firsts: dict[str, set] = __find_firsts(G)
    follows: dict[str, set] = __find_follows(G, firsts)

    for coll in G.productions: ### Por cada collección de no-terminal y su correspondiente lista de producciones
        head: Symbol = coll.head 
        for prod in coll.tails: ### Por cada producción X -> W
            current_first = __find_first(prod, firsts)
            for ter in G.terminals:
                if ter.identifier != 'eps':
                    if ter.identifier not in table.keys(): ### Iniializar dict
                        table[ter.identifier] = {}
    
                    if head.identifier not in table[ter.identifier].keys(): ### Inicializar list
                            table[ter.identifier][head.identifier] = []
    
                    if 'eps' in prod[0].identifier and ter.identifier in follows[head.identifier] or ter.identifier in current_first: ### Si X → e y t ∈ Follow (X) entonces T [X , t] = X → e. o Si X → W y t ∈ First(W) entonces T [X , t] = X → W .
                        if len(table[ter.identifier][head.identifier]) == 0:
                            table[ter.identifier][head.identifier] = prod
                        
                        else : return False, None
    return True, table
                        
                    


                    

                    

                