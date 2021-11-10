from grammar import Grammar
from ll1_table_builder import build_LL1_table
from own_token import *


def non_recursive_parse(G: Grammar, tokens: list[Token]) -> bool:
    eof_appended = False
    stack: list[str] = []
    stack.append(G.initial_nt)
    current_token_index = 0
    is_ll1, ll_table = build_LL1_table(G)

    if is_ll1:
        while len(stack) > 0 and current_token_index < len(tokens):
            gram_symbol = stack.pop()
            current_token = tokens[current_token_index]

            if gram_symbol in G.terminals: # Si es un terminal
                current_token_index += 1  # Consumir el Token
                if (isinstance(current_token, Number) and gram_symbol != 'integer') or (isinstance(current_token, Symbol) and gram_symbol != current_token.value):
                    return False

            elif gram_symbol in G.non_terminals:  # Si es un no-terminal
                prod = []
                if isinstance(current_token, Number): # Si es un número
                    prod = ll_table['integer'][gram_symbol]

                elif isinstance(current_token, Symbol): # Si es un símbolo 
                    prod = ll_table[current_token.value][gram_symbol]

                if not eof_appended and current_token_index == len(tokens) - 1: # Si ya se han leído todos los tokens, agregar eof en el fondo de la pila
                    stack.insert(0, '$')
                    eof_appended = True

                if len(prod) == 0: # Si no hay producción válida en la tabla
                    return False

                if 'epsilon' in prod: 
                    continue

                for elem in reversed(prod): # Agregar a la pila los elementos de la producción
                    stack.append(elem)

        return len(stack) == 0 and current_token_index == len(tokens) 
    return False
