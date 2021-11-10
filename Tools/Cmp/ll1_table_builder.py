from grammar import Grammar

def __find_firsts(G) -> dict[str, set]: ### Para calcular los firsts de cada no-terminal
    firsts: dict[str, set] = {}
    for ter in G.terminals: ### Calculando los first de cada terminal
        firsts[ter] = set()
        firsts[ter].add(ter)

    for noter in G.non_terminals:
        firsts[noter] = set() ### Inicializando los sets para almacenar los firsts de los no terminales

    changed = True

    while changed: ### Mientras cambie algún first 
        changed = False
        for nt, prods in G.productions.items(): ### Por cada no terminal y su correspondiente lista de producciones
            for prod in prods: ### Por cada producción X -> W
                if 'epsilon' in prod: ### Si es X -> epsilon
                    contains = True if 'epsilon' in firsts[nt] else False
                    if not contains: 
                        firsts[nt].add('epsilon')
                        changed = True

                else: ### Si es X -> W : W != epsilon
                    all_epsilon = True
                    for elem in prod:
                        contains = True if firsts[elem].issubset(firsts[nt]) else False
                        if not contains:
                            firsts[nt] = firsts[nt].union(firsts[elem])
                            changed = True

                        if 'epsilon' not in firsts[elem]:
                            all_epsilon = False
                            break
                    
                    if all_epsilon:
                        contains = True if 'epsilon' in firsts[nt] else False
                        if not contains:
                            firsts[nt].add('epsilon')
                            changed = True
    return firsts
        
def __find_first (symbols, firsts) -> set[str]: ### Para calcular el first de cualquier forma oracional
    result = set()
    all_epsilon = True
    for elem in symbols:
        result = result.union(firsts[elem])
        if 'epsilon' not in firsts[elem]:
            all_epsilon = False
            break
    
    if all_epsilon:
        result.add('epsilon')
    
    return result

def __find_follows(G, firsts) -> dict[str, set]: ### Para calcular los follow
    follows: dict[str, set] = {}

    for nt in G.non_terminals:
        follows[nt] = set()

    follows[G.initial_nt].add('$')

    changed = True
    while changed:
        changed = False
        for nt, prods in G.productions.items(): ### Por cada no terminal y su correspondiente lista de producciones
            for prod in prods: ### Por cada producción X -> W
                for i in range(len(prod)): ### Por cada símbolo en la parte derecha de la producción
                    temp = prod[i]

                    if temp in G.terminals: ### Si es un terminal
                        continue

                    first1: set[str] = __find_first(prod[i+1::], firsts)
                    first2 = first1.copy()
                    
                    if 'epsilon' in first1:
                        first1.remove('epsilon')
                    contains_all1 = True if first1.issubset(follows[temp]) else False
                    
                    if not contains_all1:
                        follows[temp] = follows[temp].union(first1)
                        changed = True
                    
                    if 'epsilon' in first2 or i == len(prod) - 1:
                        contains_all2 = True if follows[nt].issubset(follows[temp]) else False
                        if not contains_all2:
                            follows[temp] = follows[temp].union(follows[nt])
                            changed = True
    return follows

def build_LL1_table(G: Grammar) -> tuple[bool, dict[str, dict[str, list[list[str]]]]]: ### Intenta construir la tabla LL (la salida depende de si la grámatica es LL(1))
    
    table: dict[str, dict[str, list[str]]] = {}
    firsts: dict[str, set] = __find_firsts(G)
    follows: dict[str, set] = __find_follows(G, firsts)

    for nt, prods in G.productions.items(): ### Por cada no terminal y su correspondiente lista de producciones
        for prod in prods: ### Por cada producción X -> W
            current_first = __find_first(prod, firsts)
            for ter in G.terminals:
                if ter not in table.keys(): ### Iniializar dict
                    table[ter] = {}

                if nt not in table[ter].keys(): ### Inicializar list
                        table[ter][nt] = []

                if 'epsilon' in prod and ter in follows[nt] or ter in current_first: ### Si X → e y t ∈ Follow (X) entonces T [X , t] = X → e. o Si X → W y t ∈ First(W) entonces T [X , t] = X → W .
                    if len(table[ter][nt]) == 0:
                        table[ter][nt] = prod
                    
                    else : return False, None
    return True, table
                        
                    


                    

                    

                