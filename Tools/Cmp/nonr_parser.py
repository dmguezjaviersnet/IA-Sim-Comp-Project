from grammar import Grammar
from ll1_table_builder import build_LL1_table
from non_terminal import Non_terminal
from own_symbol import Symbol
from own_token import *
from terminal import Terminal


def __new_nodes(prod: list[Symbol]) -> list[Symbol]: # Crear nuevos nodos para el árbol de derivación
    new_cst_nodes: list[Symbol] = [] # cst_nodes: nodos de árbol de sintaxis concreta (o de derivación)
    for elem in prod:
        if isinstance(elem, Terminal):
            new_cst_nodes.append(Terminal(elem.identifier, *elem.attrs))

        elif isinstance(elem, Non_terminal):
            new_cst_nodes.append(Non_terminal(elem.identifier, *elem.attrs))

    return new_cst_nodes

def non_recursive_parse(G: Grammar, tokens: list[Token]) -> bool:
    eof_appended = False
    stack: list[Symbol] = []
    stack.append(G.initial_nt)
    current_token_index = 0
    is_ll1, ll_table = build_LL1_table(G)

    if is_ll1:
        while len(stack) > 0 and current_token_index < len(tokens):
            gram_symbol = stack[len(stack) - 1]
            if(gram_symbol.ast != None): stack.pop()
            current_token = tokens[current_token_index]
            
            if isinstance(gram_symbol, Terminal): # Si es un terminal
                current_token_index += 1  # Consumir el Token
                if (isinstance(current_token, Number) and gram_symbol.identifier != 'i') or (isinstance(current_token, Op) and gram_symbol.identifier != current_token.value):
                    return False

            elif isinstance(gram_symbol, Non_terminal):  # Si es un no-terminal
                prod = []
                if isinstance(current_token, Number): # Si es un número
                    prod = __new_nodes(ll_table['i'][gram_symbol.identifier])

                elif isinstance(current_token, Op): # Si es un operador
                    prod = __new_nodes(ll_table[current_token.value][gram_symbol.identifier])

                if not eof_appended and current_token_index == len(tokens) - 1: # Si ya se han leído todos los tokens, agregar eof en el fondo de la pila
                    stack.insert(0, '$')
                    eof_appended = True

                if len(prod) == 0: # Si no hay producción válida en la tabla
                    return False

                if 'eps' in prod: # Si la produción es X -> eps no se hace nada
                    continue

                for elem in reversed(prod): # Agregar a la pila los elementos de la producción (nuevos nodos del árbol de derivación)
                    stack.append(elem)

        return len(stack) == 0 and current_token_index == len(tokens)
    return False
