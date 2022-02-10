from pickle import NONE
from typing import Any, Dict, FrozenSet, List, Set, Tuple
from automaton.state import State
from parser.grammar import Grammar
from parser.non_terminal import Non_terminal
from parser.own_token import Token, Token_Type
from parser.lr0_item import Lr0_item
from parser.lr1_item import Lr1_item
from parser.own_symbol import Symbol
from parser.terminal import Terminal
from parser.ll1_table_builder import find_first, find_firsts
from parser.action_goto_table import Action_Goto_Table
from parser.eval_rule import eval_rule
from errors import OrbisimParserError
from tools import serialize_data, deserialize_data

action_goto_table: Action_Goto_Table = None
lr1_states_hash_table = None

__is_atom = lambda token : (token.token_type == Token_Type.int or token.token_type == Token_Type.float or
    token.token_type == Token_Type.string or token.token_type == Token_Type.boolean or 
    token.token_type == Token_Type.id_orbsim or token.token_type == Token_Type.type_id_orbsim)

def __get_key(val: str, coll: Dict[Token_Type, str]):
    for key, value in coll.items():
        if value == val:
            return key

def __build_lr0_items(G: Grammar) -> List[Lr0_item]:
    lr0_items: List[Lr0_item] = []

    # Construyendo centros
    for coll in G.productions:
        head = coll.head
        for tail in coll.tails:
            for index, _ in enumerate(tail):
                if 'eps' not in tail[0].identifier:
                    lr0_items.append(Lr0_item(head, tuple(tail), index))

                else : lr0_items.append(Lr0_item(head, (), index))

            lr0_items.append(Lr0_item(head, tuple(tail), len(tail)))
    
    return lr0_items

def __lr1_automaton_clousure(G: Grammar, state: State, lr0_items: List[Lr0_item], firsts: Dict[str, Set]) -> bool:
    state_id_number = int(state.id)
    current_lr1_item_pos = 0

    lr1_items_hash_record = []

    while current_lr1_item_pos < len(state.lr1_items):
        current_lr1_item: Lr1_item = state.lr1_items[current_lr1_item_pos]
        frozen_set_iter = iter(current_lr1_item.look_ahead)
        curr_frozen_set_elem = next(frozen_set_iter)

        if current_lr1_item.center.dot < len(current_lr1_item.center.tail):
            curr_item_symbol_after_dot: Symbol = current_lr1_item.center.tail[current_lr1_item.center.dot]

            if isinstance(curr_item_symbol_after_dot, Terminal):
                current_lr1_item_pos += 1
                continue
            
            remaining_item_center = tuple([current_lr1_item.center.tail[index] for index in range (current_lr1_item.center.dot + 1, len(current_lr1_item.center.tail))])
            look_aheads = tuple([Symbol(elem) for elem in current_lr1_item.look_ahead])
            remaining_first = find_first(remaining_item_center + look_aheads, firsts)

            if 'eps' in remaining_first:
                remaining_first.remove('eps')
                remaining_first = remaining_first.union(current_lr1_item.look_ahead)

            for lr0_item in lr0_items:
                if lr0_item.dot == 0 and lr0_item.head.identifier == curr_item_symbol_after_dot.identifier:
                    for elem in remaining_first:
                        new_look_ahead: FrozenSet[str] = frozenset([elem])
                        new_lr1_item = Lr1_item(lr0_item, new_look_ahead)
                        new_lr1_item_hash = hash(new_lr1_item)
                        if new_lr1_item_hash not in lr1_items_hash_record:
                            state.lr1_items.append(new_lr1_item)
                            lr1_items_hash_record.append(new_lr1_item_hash)

        current_lr1_item_pos += 1
    
    state.lr1_items = tuple(state.lr1_items)

    new_state_hash = hash(state.lr1_items)
    state.hash = new_state_hash
    if new_state_hash in lr1_states_hash_table:
        state_id_number = int(lr1_states_hash_table[new_state_hash].id)
    
    current_lr1_item_pos = 0
    while(current_lr1_item_pos < len(state.lr1_items)):
        current_lr1_item: Lr1_item = state.lr1_items[current_lr1_item_pos]
        prod_id =  None
        frozen_set_iter = iter(current_lr1_item.look_ahead)
        curr_frozen_set_elem = next(frozen_set_iter)

        if current_lr1_item.center.dot == len(current_lr1_item.center.tail):
            if current_lr1_item.center.head.identifier != 'S\'':
                prod_id = (G.map_prodstr_rules[str(current_lr1_item.center)][0] 
                            if current_lr1_item.center.tail
                            else G.map_prodstr_rules[str(current_lr1_item.center) + 'eps '][0])
                            
                if state_id_number not in action_goto_table.terminals_dict[curr_frozen_set_elem]:
                    action_goto_table.terminals_dict[curr_frozen_set_elem][state_id_number] = None
                
                if action_goto_table.terminals_dict[curr_frozen_set_elem][state_id_number] == None:
                    action_goto_table.terminals_dict[curr_frozen_set_elem][state_id_number] = ('Reduce', prod_id)
                
                elif action_goto_table.terminals_dict[curr_frozen_set_elem][state_id_number] == ('Reduce', prod_id):
                    current_lr1_item_pos += 1
                    continue
                
                else: return False
            
            else:
                action_goto_table.terminals_dict['$'][state_id_number] = ('OK', -1)
            
        current_lr1_item_pos += 1

    return True

def __lr1_automaton_goto(G: Grammar, state: State, symbol: Symbol, new_id: int, lr0_items: List[Lr0_item], firsts: Dict[str, Set]) -> Tuple[bool, State]:
    new_lr1_state = State(f'{new_id}', is_final_state=True)
    new_lr1_state.__setattr__('lr1_items', [])

    for lr1_item in state.lr1_items:
        if lr1_item.center.dot < len(lr1_item.center.tail):
            if symbol.identifier == lr1_item.center.tail[lr1_item.center.dot].identifier:
                new_lr1_state.lr1_items.append(Lr1_item(Lr0_item(lr1_item.center.head, lr1_item.center.tail, lr1_item.center.dot + 1), lr1_item.look_ahead))

    no_conflict = __lr1_automaton_clousure(G, new_lr1_state, lr0_items, firsts)

    return no_conflict, new_lr1_state if new_lr1_state.lr1_items else None

def __build_lr1_automaton(G: Grammar, lr0_items: List[Lr0_item]) -> Tuple[bool, State, List[State]]:
    global action_goto_table
    global lr1_states_hash_table

    action_goto_table = Action_Goto_Table(G.terminals, G.non_terminals)
    lr1_states_hash_table = {}

    firsts: Dict[str, Set] = find_firsts(G) # Computando Firsts
    initial_state = State('1', is_final_state=True)
    initial_lr1_item = Lr1_item(Lr0_item(Non_terminal('S\''), (G.initial_nt, ), 0), frozenset({'$'}))
    initial_state.lr1_items = [initial_lr1_item]

    __lr1_automaton_clousure(G, initial_state, lr0_items, firsts)
    initial_lr1_item_hash = hash(initial_state.lr1_items)
    lr1_states_hash_table[initial_lr1_item_hash] = initial_state

    symbols: List[Symbol] = G.terminals + G.non_terminals
    states_goto_not_calculated = [initial_state]

    new_state_id = 2
    while (states_goto_not_calculated):
        current_state = states_goto_not_calculated.pop(0)
        current_state_id_number = int(current_state.id)

        for symbol in symbols:
            no_conflict, new_lr1_state = __lr1_automaton_goto(G ,current_state, symbol, new_state_id, lr0_items, firsts)
            if no_conflict:
                if new_lr1_state:
                    if new_lr1_state.hash in lr1_states_hash_table:
                        new_lr1_state = lr1_states_hash_table[new_lr1_state.hash]

                    else:
                        lr1_states_hash_table[new_lr1_state.hash] = new_lr1_state
                        states_goto_not_calculated.append(new_lr1_state)
                        new_state_id += 1
                    
                    current_state.transitions[symbol.identifier] = new_lr1_state

                    new_id = int(lr1_states_hash_table[new_lr1_state.hash].id)
                    if isinstance(symbol, Terminal):
                        if current_state_id_number not in action_goto_table.terminals_dict[symbol.identifier]:
                            action_goto_table.terminals_dict[symbol.identifier][current_state_id_number] = None

                        if action_goto_table.terminals_dict[symbol.identifier][current_state_id_number] == None:
                            action_goto_table.terminals_dict[symbol.identifier][current_state_id_number] = ('Shift', new_id)

                        else : return False, None, None

                    elif isinstance(symbol, Non_terminal):
                        if current_state_id_number not in action_goto_table.non_terminals_dict[symbol.identifier]:
                            action_goto_table.non_terminals_dict[symbol.identifier][current_state_id_number] = 0

                        if action_goto_table.non_terminals_dict[symbol.identifier][current_state_id_number] == 0:
                            action_goto_table.non_terminals_dict[symbol.identifier][current_state_id_number] = new_id
                        
                        else: return False, None, None

                continue
            
            return False, None, None

    return True, initial_state, [state for _, state in enumerate(lr1_states_hash_table.values())]

def lr1_parse(G: Grammar, tokens: List[Token], token_type_to_string: Dict[Token_Type, str]) -> Tuple[bool, Any]:
    lr0_items = __build_lr0_items(G)
    is_lr1, lr1_automaton, states = False, None, None

    global action_goto_table    
    del globals()['lr1_states_hash_table']
    del lr1_automaton

    deserialized_action_goto_table = deserialize_data('./serialized_data/serialized_action_goto_table.pickle')
    deserialized_states = deserialize_data('./serialized_data/states.pickle')

    if deserialized_states != None:
        states = deserialized_states
    
    if deserialized_action_goto_table != None:
        is_lr1 = True
        action_goto_table = deserialized_action_goto_table

    else:
        is_lr1, lr1_automaton, states = __build_lr1_automaton(G, lr0_items)

        if is_lr1:
            serialize_data(action_goto_table, './serialized_data/serialized_action_goto_table')
            serialize_data(states, './serialized_data/states')

    symbols_stack = []
    states_stack = [states[0]]
    prods = list(G.map_prodstr_rules.keys())
    parsing_errors: OrbisimParserError = []

    curr_token_index = 0

    if is_lr1:
        while (symbols_stack or states_stack) and curr_token_index < len(tokens):
            curr_token = tokens[curr_token_index]

            if curr_token.token_type == Token_Type.space or curr_token.token_type == Token_Type.new_line:
                curr_token_index += 1
                continue
            
            curr_token_symbol_identifier = token_type_to_string[curr_token.token_type]
            curr_state = states_stack[-1]
            curr_state_id = int(curr_state.id)

            if curr_state_id in action_goto_table.terminals_dict[curr_token_symbol_identifier]:
                action, state_or_prod_id = action_goto_table.terminals_dict[curr_token_symbol_identifier][curr_state_id]

                if action == 'Shift':
                    new_terminal = Terminal(curr_token_symbol_identifier)

                    if __is_atom(curr_token):
                        new_terminal.val = curr_token.lexeme

                    symbols_stack.append(new_terminal)
                    states_stack.append(states[state_or_prod_id - 1])
                    curr_token_index += 1

                elif action == 'Reduce':
                    prod_str = prods[state_or_prod_id - 1]
                    prod_length = G.map_prodstr_rules[prod_str][1]
                    tail = []
                    while prod_length:
                        states_stack.pop()
                        tail.append(symbols_stack.pop())
                        prod_length -= 1

                    tail = tail[::-1]
                    head_str = prod_str.split(' ')[0]
                    head = Non_terminal(head_str, 'ast')

                    if not parsing_errors:
                        rule, _ = G.map_prodstr_rules[prod_str][2][0]
                        eval_rule(rule, head, tail)

                    symbols_stack.append(head)
                    state_after_reduce = action_goto_table.non_terminals_dict[head_str][int(states_stack[-1].id)]
                    states_stack.append(states[state_after_reduce - 1])

                elif action == 'OK':
                    return parsing_errors, symbols_stack.pop().ast
                    
            elif not curr_token_symbol_identifier in curr_state.transitions:
                expected_token = ''
                for _, elem in enumerate(curr_state.transitions):          
                    expected_token = elem
                    break
                      
                parsing_errors.append(OrbisimParserError(f'expected token ------> {expected_token}'))
                return parsing_errors, None 

    return parsing_errors, None