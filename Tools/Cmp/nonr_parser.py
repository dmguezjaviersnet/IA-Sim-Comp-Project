from typing import Callable
from grammar import Grammar
from ll1_table_builder import build_LL1_table
from non_terminal import Non_terminal
from own_symbol import Symbol
from own_token import *
from terminal import Terminal
from rules import eval_rule

def __eval_sintetized_rules(head: Symbol, tail: list[Symbol] ,rules: list[tuple[Callable, bool]]):
    for rule, is_sintetized in rules:
        if is_sintetized:
            eval_rule(rule, head, tail)

def __eval_inherited_rules(head: Symbol, tail: list[Symbol] ,rules: list[tuple[Callable, bool]]):
    for rule, is_sintetized in rules:
        if not is_sintetized:
            eval_rule(rule, head, tail)


def __append_ids(rule_key, ids: list[Symbol]):
    for elem in ids:
        rule_key += elem.identifier + ' '
    return rule_key

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
    stack: list[Symbol, str] = []
    stack.append((None, G.initial_nt, '', None))
    current_token_index = 0
    is_ll1, ll_table = build_LL1_table(G)
    ast_answer = None

    if is_ll1:
        while len(stack) > 0 and current_token_index < len(tokens):

            head, current_symbol, prod_id, prod = stack[len(stack) - 1]
            rule_key = current_symbol.identifier + ' -> '
            current_token = tokens[current_token_index]

            if current_symbol.identifier == '$': # EOF
                stack.pop()
                current_token_index += 1

            elif current_symbol == G.initial_nt and current_symbol.ast != None: # Ya está computado el ast en el atributo ast del token inicial de la gramática
                ast_answer = current_symbol.ast
                stack.pop()

            elif isinstance(current_symbol, Terminal) or current_symbol == 'eps': # Si el símbolo es un terminal
                if current_symbol.identifier == 'i':
                    current_symbol.val = current_token.value
                    
                stack.pop()
                __eval_sintetized_rules(head, prod, G.map_prodstr_rules[prod_id])
                
                if current_symbol.identifier == 'eps':
                    continue

                current_token_index += 1  # Consumir el Token
                if (isinstance(current_token, Num) and current_symbol.identifier != 'i') or (isinstance(current_token, Op) and current_symbol.identifier != current_token.value):
                    return False

            elif prod != None and current_symbol == prod[len(prod) - 1] and current_symbol.ast != None: # # Si es un no-terminal ya computado
                __eval_sintetized_rules(head, prod, G.map_prodstr_rules[prod_id])
                stack.pop()

            else:  # Si es un no-terminal aún no computado
                if current_symbol.ast != None:
                    __eval_inherited_rules(head, prod, G.map_prodstr_rules[prod_id])
                    stack.pop()
                    continue
                
                prod = []
                if isinstance(current_token, Num): # Si el token es un número
                    prod = __new_nodes(ll_table['i'][current_symbol.identifier])
                    rule_key = __append_ids(rule_key, prod)

                elif isinstance(current_token, Op): # Si el token es un operador
                    prod = __new_nodes(ll_table[current_token.value][current_symbol.identifier])
                    rule_key = __append_ids(rule_key, prod)

                if not eof_appended and current_token_index == len(tokens) - 1: # Si ya se han leído todos los tokens, agregar eof en el fondo de la pila
                    stack.insert(0, (None, Terminal('$'), '', None))
                    eof_appended = True

                if len(prod) == 0: # Si no hay producción válida en la tabla
                    return False

                for elem in reversed(prod): # Agregar a la pila los elementos de la producción (nuevos nodos del árbol de derivación)
                    stack.append((current_symbol, elem, rule_key, prod))

        return ast_answer, len(stack) == 0 and current_token_index == len(tokens)
    return False
