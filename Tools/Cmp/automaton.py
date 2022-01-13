from typing import Dict, List, Set, Tuple

from tools import*

class Automaton:

    '''Representa un autómata con todas sus características'''

    @property
    def number_of_states(self):
        return len(self.states)

    def __init__(self, nStates: int, q0: int, finalStates: List[int], transitions, statesList=[]):
        
        # if not len(statesList):
        #     states = []
        
        #     for i in range(nStates):
        #         state = State(i, f"q{i}", i in finalStates)
        #         states.append(state)
            
        #     self.states = states
        
        # else:
        #     self.states = statesList
        
        
       

        self.q0 = q0
        self.finals = set(finalStates)
    
        self.vocabulary: Set = set()
        self.transitions = {state: {} for state in range(self.number_of_states)}

        for (origin,symbol), destinations in transitions.items():
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)

        self.vocabulary.discard(EPSILON) # remove epsilon from vocabulary 
        
class NFA(Automaton):
    
    '''Autómata no-determinista'''

    def __init__ (self, nStates, q0, finalStates, transitions, statesList = []):
        super().__init__(nStates, q0, finalStates, transitions, statesList)
    
    def epsilonTransitions(self, state):
        print(self.transitions)
        if state in self.transitions and EPSILON in self.transitions[state]: 
            return self.transitions[state][EPSILON]
        else:
            return []
    

    def __str__(self) -> str:
        return f" Number of States:{self.number_of_states}\n q0:{self.q0}\nTransitions:{self.transitions}\n finalStates={self.finals}"

class DFA(Automaton):

    '''Autómata determinista'''

    def __init__(self, nStates: int, q0: int, finalStates: List[int],  transitions, statesList = []):
        
        temp: Dict = {}
        for i, j in transitions.items():
            for k,l in j.items():
                temp[(i,k)] = l
        
        self.currentState = q0
        super().__init__(nStates, q0, finalStates, temp, statesList)
    

    def __str__(self) -> str:
        return f"States: {self.states}\n q0:{self.q0} \n Final States: {self.finals} \n Transitions: {self.transitions} \n Vocabulary: {self.vocabulary} "

    def _move_next_state(self, symbol):
        self.currentState = self.transitions[self.currentState][symbol]

    def _reset_current_state(self):
        self.currentState = self.q0
    
    def match(self, word):
        self._reset_current_state()

        for s in word:
            try:
                self._move_next_state(s)
            except KeyError:
                return False

        return self.currentState in self.finals

class StatesContainer:

    def __init__(self, values, automaton: 'NFA', id: int = -1):
        self.elems = set(values)
        self.id = id
        self.tag = [f"q{e} " for e in self.elems] 
        self.isFinal = any(s in automaton.finals for s in self.elems)
        
    def add(self, value):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)
    
    def __iter__(self):
        return iter(self.set)