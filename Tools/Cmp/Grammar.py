from typing import List
from Non_terminal import *
from Terminal import *
from Production import *


class Grammar: # Clase para representar una gramática

    def __init__(self, terminals, non_terminals: List[Terminal], initial_nt: List[Non_terminal], productions: List[Production]): # Ctor
        self.terminals = terminals # terminales
        self.non_terminals = non_terminals # no-terminales
        self.initial_nt = initial_nt # token inicial de la gramática
        self.productions = productions # producciones

        self.map_prodstr_rules: dict[str, tuple[Callable, bool]] = self.__map_rules() # Para cada producción X -> W mapear en un diccionario las reglas que le corresponden

    def __map_rules(self): # Método para mapear el string que identifica a una producción con las reglas que le corresponden
        ans: dict[str, tuple[Callable, bool]] = {}
        
        for i in range(len(self.productions)): # Por cada no-terminal
            head_id = self.productions[i].head.identifier + ' -> ' # id de la cabeza de la producción
            for j in range(len(self.productions[i].tails)): # Por cada producción de este no terminal
                tail_id = ''
                for elem in self.productions[i].tails[j]: # Por cada elemento en esta producción
                    tail_id += elem.identifier + ' ' # Añadirlo al id de la cola de la producción
                ans[head_id + tail_id] = self.productions[i].rules[j] # Asignarle al id de la producción la regla correspondiente
        return ans