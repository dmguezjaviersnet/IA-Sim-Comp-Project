from typing import Any, List, Tuple

from Automata.automaton import Automaton, State
from Grammar import Grammar
from Non_terminal import Non_terminal
from Own_token import Token
from Lr0_item import Lr0_item
from Lr1_item import Lr1_item

def __build_lr0_items(G: Grammar) -> List[Lr1_item]:
    lr0_items: List[Lr0_item] = []

    # Construyendo centros
    for coll in G.productions:
        head = coll.head
        for tail in coll.tails:
            for index, _ in enumerate(tail):
                lr0_items.append(Lr0_item(head, tail, index))
            lr0_items.append(Lr0_item(head, tail, len(tail)))
    
    return lr0_items

def __build_lr1_automaton (G: Grammar, lr0_items: Lr0_item):

    initial_lr1_item = Lr1_item(Lr0_item(Non_terminal('S'), G.initial_nt, 0), {'$'})

def lr1_parser (G: Grammar, tokens: List[Token]) -> Tuple[bool, Any]:
    lr0_items = __build_lr0_items(G)
    lr1_automaton = __build_lr1_automaton(lr0_items)
