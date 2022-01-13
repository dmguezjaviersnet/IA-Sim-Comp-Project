from typing import Any, Callable, List, Tuple

from Grammar import Grammar
from ll1_table_builder import build_LL1_table
from Non_terminal import Non_terminal
from Own_symbol import Symbol
from Own_token import *
from Terminal import Terminal
from test_grammar_rules import eval_rule


def __eval_rules(head: Symbol, tail: List[Symbol], rules: List[Tuple[Callable, bool]], eval_sintetized: bool): # Evaluar las reglas correspondientes
    for rule, is_sintetized in rules: # Por cada regla correspondiente a esta producción
        if eval_sintetized: # Si hay que evaluar sintetizadas
            if is_sintetized: # Y la regla es sintetizada
                eval_rule(rule, head, tail) # Evaluar la regla

        elif not is_sintetized: # Si hay que evaluar heredadas
            if not is_sintetized: # Y la regla es heredada
                eval_rule(rule, head, tail) # Evaluar la regla


def __append_ids(rule_key, ids: List[Symbol]): # Método para construir el string que identifica a una producción X -> W y usarlo para poder obtener las reglas de dicha producción usando un Dict
    for elem in ids: # Por cada elemento en la producción
        rule_key += elem.identifier + ' ' # Añadimos a X ->, el string correspondiente del elemento para ir formando la llave que usaremos en el Dict
    return rule_key


def __new_nodes(prod: List[Symbol]) -> List[Symbol]: # Crear nuevos nodos para el árbol de derivación
    # cst_nodes: nodos de árbol de sintaxis concreta (o de derivación)
    new_cst_nodes: List[Symbol] = [] # Inicializando la lista donde vamos a almacenar los nuevos nodos
    for elem in prod: # Por cada elemento de la producción 
        if isinstance(elem, Terminal): # Si es un terminal
            new_cst_nodes.append(Terminal(elem.identifier, *elem.attrs)) # Añadir el nuevo terminal correspondiente

        elif isinstance(elem, Non_terminal): # Si es un no-terminal
            new_cst_nodes.append(Non_terminal(elem.identifier, *elem.attrs)) # Añadir el nuevo no-terminal correspondiente

    return new_cst_nodes


def non_recursive_parse(G: Grammar, tokens: List[Token]) -> Tuple [Any, bool]: # Parser predictivo no recursivo (LL)
    eof_appended = False # Si ya añadimos eof a la pila
    stack: List[tuple[Symbol, Symbol, str, List[Symbol]]] = [] # Una pila para ir guardando tuplas (cabeza de la producción, símbolo que se está analizando, id de la producción, producción)
    stack.append((None, G.initial_nt, '', None)) # Inicialmente en la pila está una tupla con el símbolo inicial de la gramática y el resto de los valores de la tupla tienen valores que no afecten el algoritmo
    current_token_index = 0 # Índice en la lista tokens, del token actual que estamos analizando
    is_ll1, ll_table = build_LL1_table(G) # Computemos si la gramática es LL(1) y en caso de que lo sea obtengamos la tabla LL
    ast_answer = None # Aquí almacenaremos el AST que retornaremos al final

    if is_ll1: # Si la gramática es LL(1) es que se puede parsear con este algoritmo
        while len(stack) > 0 and current_token_index < len(tokens): # Mientras la pila no esté vacía

            head, current_symbol, prod_id, prod = stack[-1] # Obtengamos el elemento que está en el tope de la pila
            rule_key = f'{current_symbol.identifier} -> ' # Asignamos la llave para la regla de la producción que se vaya a aplicar, inicialmente como X ->, donde X es el el id del elemento actual
            current_token = tokens[current_token_index] # Guardemos el token que estamos analizando

            if current_symbol.identifier == '$':  # Si lo que hay en el tope de la pila es $ (EOF), entonces ya terminé de parsear y después de este token no hay más tokens por analizar
                stack.pop() # Vacíamos lo pila, pues solo había un elemente en ella
                current_token_index += 1 # Y nos desplazamos hacia el próximo token, que va a ser ninguno, pues ya no hay más nada por analizar

            elif current_symbol == G.initial_nt and current_symbol.ast != None: # Si ya está computado el ast en el atributo ast del token inicial de la gramática
                ast_answer = current_symbol.ast # Entonces el AST ya está computado y lo guardamos en esta variable para devolverlo
                stack.pop() # Sacamos el elemento inicial de la gramática de la pila

            elif isinstance(current_symbol, Terminal) or current_symbol == 'eps': # Si el símbolo es un terminal
                if current_symbol.identifier == 'character': # Y es un caracter
                    current_symbol.val = current_token.lexeme # Almacenamos su valor

                stack.pop() # Sacamos de la pila el terminal
                __eval_rules(head, prod, G.map_prodstr_rules[prod_id], True) # Evaluar reglas sintetizadas

                if current_symbol.identifier == 'eps':  # Si era epsilon
                    continue # Entonces no se consume ningún token

                current_token_index += 1  # Consumir el Token
                if  ((current_token.tkn_type == Token_Type.character and current_symbol.identifier != 'character') or
                     (current_token.is_operator() and current_symbol.identifier != current_token.lexeme)):

                    return None, False

            elif prod != None and current_symbol == prod[len(prod) - 1] and current_symbol.ast != None: # Si es el último no-terminal de la producción y ya está computado su AST
                __eval_rules(head, prod, G.map_prodstr_rules[prod_id], True) # Evaluar reglas sintetizadas
                stack.pop() # Sacar de la pila el no-terminal

            else:  # Si no es último no-terminal de la producción y ya está computado
                if current_symbol.ast != None: # Y ya se computó el AST del no-terminal actual
                    __eval_rules(head, prod, G.map_prodstr_rules[prod_id], False) # Evaluar reglas heredadas
                    stack.pop() # Sacar de la pila el no-terminal
                    continue # Pasar al próximo elemento de la pila, pues ya se aplicó la producción con este no-terminal y regresó el algoritmo

                elif head != None: # Si el no-terminal cabecera de la producción no es vacio
                    __eval_rules(head, prod, G.map_prodstr_rules[prod_id], False) # Evaluar reglas heredadas y continuar a aplicar producciones

                prod = [] # Producción
                if current_token.tkn_type == Token_Type.character:  # Si el token es un número
                    prod = __new_nodes(
                        ll_table['character'][current_symbol.identifier]) # Almacenar la producción
                    rule_key = __append_ids(rule_key, prod) # Construir la llave que nos permita obtener las reglas de la producción que se aplicó

                elif current_token.is_operator():  # Si el token es un operador
                    prod = __new_nodes(
                        ll_table[current_token.lexeme][current_symbol.identifier])
                    rule_key = __append_ids(rule_key, prod) # Construir la llave que nos permita obtener las reglas de la producción que se aplicó

                if not eof_appended and current_token_index == len(tokens) - 1: # Si ya se han leído todos los tokens
                    stack.insert(0, (None, Terminal('$'), '', None)) # Agregar eof en el fondo de la pila
                    eof_appended = True # Indicar que ya agregamos EOF en la pila

                if len(prod) == 0:  # Si no hay producción válida en la tabla
                    return None, False # Imposible de parsear

                for elem in reversed(prod): # Agregar a la pila los elementos de la producción (nuevos nodos del árbol de derivación)
                    stack.append((current_symbol, elem, rule_key, prod))
                    
        return ast_answer, len(stack) == 0 and current_token_index == len(tokens)
    return False, None
