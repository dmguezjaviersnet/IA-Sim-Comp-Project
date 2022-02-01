from typing import List, Set
from tools import EPSILON

class Automaton:

    '''
        Representa un autómata NFA con todas sus características

    '''

    
    def __init__(self, number_of_states: int, initial_state: int, finalStates: List[int], transitions):
        
        self.number_of_states = number_of_states # número de estados que va a tener el autómata

        self.initial_state = initial_state # el estado inicial del autómata
        self.finals = set(finalStates) # el conjunto de todos los estados finales del autómata
    
        self.vocabulary: Set = set() # el vocabulario del autómata(conjunto finito de símbolos que pueden aparecer en la cinta) 
        self.transitions = {state: {} for state in range(self.number_of_states)} # función de transición que dado un estado y un símbolo te da todos los posibles estados a los que te puedes mover

        for (origin,symbol), destinations in transitions.items():
            
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)

        self.vocabulary.discard(EPSILON) # quitamos del vocabulario el símbolo '' que representa las transiciones epsilons
        

    def __add__(self, other: 'Automaton'):
        return Automaton.automaton_concat(self, other)
    
    @staticmethod
    def automaton_union(a1: 'Automaton', a2: 'Automaton')-> 'Automaton':
        '''
            Devuelve la operación union entre dos autómatas
        '''
        newTransitions = {}
        newq0 = 0
        newa1start = 1
        newa2start = a1.number_of_states + 1
        newFinalState = a2.number_of_states + newa2start

        for i, j in a1.transitions.items():
               for k,l in j.items():
                   newTransitions[(i+newa1start,k)] = [x+newa1start for x in l]

        for i, j in a2.transitions.items():
               for k,l in j.items():
                   newTransitions[(i+newa2start,k)] = [x+newa2start for x in l]

        newTransitions[(newq0, EPSILON)] = [newa1start, newa2start]
        for fs in a1.finals:
            if (fs, EPSILON) not in a1.transitions:
                newTransitions[(fs+newa1start, EPSILON)] = [newFinalState]
            else:
                newTransitions[(fs+newa1start, EPSILON)].append(newFinalState)

        for fs in a2.finals:
           if (fs, EPSILON) not in a2.transitions:
               newTransitions[(fs+newa2start, EPSILON)] = [newFinalState]
           else:
               newTransitions[(fs+newa2start, EPSILON)].append(newFinalState)

        new_number_of_states = a1.number_of_states + a2.number_of_states + 2

        return Automaton(new_number_of_states, newq0, [newFinalState], newTransitions)

    @staticmethod
    def automaton_concat(a1: 'Automaton', a2: 'Automaton') -> 'Automaton':
        newTransitions = {}
        newq0 = 0
        newa1start = 0
        newa2start = a1.number_of_states
        newFinalState = a2.number_of_states + newa2start - 1

        for i, j in a1.transitions.items():
                for k,l in j.items():
                    newTransitions[(i,k)] = l

        for sf in a1.finals:
            if (sf, EPSILON) in newTransitions:
                newTransitions[sf, EPSILON].append(newa2start)
            else:
                newTransitions[ sf, EPSILON] = [newa2start]

        for i, j in a2.transitions.items():
               for k,l in j.items():
                   newTransitions[(i+newa2start,k)] = [x+newa2start for x in l]

        new_number_of_states = a1.number_of_states + a2.number_of_states
        return Automaton(new_number_of_states, newq0, [newFinalState], newTransitions)

    @staticmethod
    def automaton_closure(a1: 'Automaton')-> 'Automaton':

        newTransitions = {}
        newq0 = 0
        newa1start = 1
        newFinalState = a1.number_of_states + 2 - 1

        for i, j in a1.transitions.items():
               for k,l in j.items():
                   newTransitions[(i+newa1start,k)] = [x+newa1start for x in l]

        newTransitions[(newq0, EPSILON)] = [newa1start, newFinalState]

        for fs in a1.finals:
            if (fs, EPSILON) not in a1.transitions:
                newTransitions[(fs+newa1start, EPSILON)] = [newFinalState]
            else:
                newTransitions[(fs+newa1start, EPSILON)].append(newFinalState)

        newTransitions[(newFinalState, EPSILON)] = [newq0]
        new_number_of_states = a1.number_of_states  + 2

        return Automaton(new_number_of_states, newq0, [newFinalState], newTransitions)