from typing import Callable, Dict, List, Tuple
from parser.non_terminal import Non_terminal
from parser.terminal import Terminal
from parser.production import Production

class Grammar: # Clase para representar una gramática

    '''Clase para representar una gramática con todas sus características'''

    def __init__(self, terminals: List[Terminal], non_terminals: List[Non_terminal], initial_nt: Non_terminal, productions: List[Production]): # Ctor
        self.terminals = terminals # terminales
        self.non_terminals = non_terminals # no-terminales
        self.initial_nt = initial_nt # token inicial de la gramática
        self.productions = productions # producciones

        self.map_prodstr_rules: dict[str, Tuple[Callable, bool]] = self.__map_rules() # Para cada producción X -> W mapear en un diccionario las reglas que le corresponden

    def __map_rules(self) -> Dict[str, Tuple[int, int, Tuple[Callable, bool]]]: # Método para mapear el string que identifica a un par (head, tail) con las reglas que le corresponden
        ans: Dict[str, Tuple[int, int, Tuple[Callable, bool]]] = {}
        
        prod_id = 1
        for i, elem in enumerate(self.productions): # Por cada no-terminal
            head_str = f'{elem.head.identifier} -> ' # id de la cabeza de la producción
            for j, _ in enumerate(self.productions[i].tails): # Por cada producción de este no terminal
                tail_str = ''
                for elem in self.productions[i].tails[j]: # Por cada elemento en esta producción
                    tail_str += f'{elem.identifier} ' # Añadirlo al id de la cola de la producción
                ans[head_str + tail_str] = (prod_id, len(self.productions[i].tails[j]) if elem.identifier != 'eps' else 0, self.productions[i].rules[j]) # Asignarle al id de la producción la regla correspondiente
                prod_id += 1
        return ans

    def __str__(self) -> str:
        terms = ''
        no_terms = ''
        init_nt = f'{self.initial_nt.__str__()}\n'
        prods = ''

        for term in self.terminals:
            terms += f'{term.__str__()} '
        terms += '\n'

        for no_term in self.non_terminals:
            no_terms += f'{no_term.__str__()} '
        no_terms += '\n'

        for prod in self.productions:
            prods += f'{prod.__str__()}\n'

        return 'Grammar\n\n' + 'initial non_terminal : ' + init_nt + 'terminals: ' +  terms + 'non terminals: ' + no_terms + 'productions: \n' + prods

        



