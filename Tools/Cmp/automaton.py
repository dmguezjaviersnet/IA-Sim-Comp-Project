from typing import Dict, List, Set


EPSILON = ''

class State:
    
    '''Representa un estado de un autómata'''

    def __init__(self, id: int, tag, isFinal: bool = False):
        self.id = id
        self.tag = tag
        self.isFinal = isFinal
        self.transitions = {}
        self.epsilon_transitions  = set()
    
    def has_a_transition(self, symbol):
        return symbol in self.transitions.keys()
    
    def add_transition(self, symbol: str, state: 'State'):
        if symbol in self.transitions.keys():
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]
        return self

    def add_epsilon_transition(self, state: 'State'):
        self.epsilon_transitions.add(state)
        return self

    @staticmethod
    def move_states(symbol, *states: List['State']):
        return { s for state in states if state.has_a_transition(symbol) for s in state[symbol]}


    
    def __str__(self) -> str:
        return f"Id:{self.id}\n Tag:{self.tag} \n isFinal:{self.isFinal}"

class Automaton:

    '''Representa un autómata con todas sus características'''

    @property
    def number_of_states(self):
        return len(self.states)

    def __init__(self, nStates: int, q0: int, finalStates: List[int], transitions, statesList=[]):
        
        if not len(statesList):
            states = []
        
            for i in range(nStates):
                state = State(i, f"q{i}", i in finalStates)
                states.append(state)
            
            self.states = states
        
        else:
            self.states = statesList
        
        
       

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



def epsilonClosure(automaton:'NFA', states: List[int]):
    eClosure = set(states)
    stack = list(states)
    
    while len(stack):
        state = stack.pop()
        for eTransition in automaton.epsilonTransitions(state):
            if not eTransition in eClosure:
                stack.append(eTransition)
                eClosure.add(eTransition)
    return eClosure

#  Dado un conjunto de estados y un simbolo obtener el conjunto de estados a los cuales se puede llegar
#  si partimos de los estados iniciales
def goTo(automaton:'NFA', states: List[int], symbol: str):
    goto = set()

    for state in states:
        if state in automaton.transitions and symbol in automaton.transitions[state]:
            goto.update(automaton.transitions[state][symbol])
    
    return goto

@staticmethod
def NFAtoDFA(automaton: 'NFA'):
    transitions = {}

    q0 = StatesContainer(epsilonClosure(automaton, [automaton.q0]),automaton, 0)

    stack = [q0]
    statesforDFA: List[StatesContainer] = [q0]
    listSort = [i for i in automaton.vocabulary]
    listSort.sort()
    while len(stack):
        current = stack.pop()
        for symbol in listSort:
            nextGoTo = goTo(automaton,current.elems,symbol)
            newEClosure = epsilonClosure(automaton, nextGoTo)

            if len(newEClosure):
                qi = StatesContainer(newEClosure, automaton, len(statesforDFA))
                
                for state in statesforDFA:
                    if state.elems == newEClosure:
                        qi = state
              
                    
                if current.id not in transitions: 
                    transitions[current.id] = {}
                if  symbol in transitions[current.id]:
                    Exception('not DFA from NFA')
                else:
                    transitions[current.id][symbol] = qi.id

                if qi not in statesforDFA:
                    stack.append(qi)
                    statesforDFA.append(qi)
    
    finals = [ s.id for s in statesforDFA if s.isFinal]
    
    statesList = [State(i.id, i.tag, i.isFinal) for i in statesforDFA]

    return DFA(nStates = len(statesforDFA), q0 = 0, finalStates = finals, transitions = transitions, statesList = statesList)


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
    

def AutomatonUnion(a1: NFA, a2: NFA):

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
    
    return NFA(new_number_of_states, newq0, [newFinalState], newTransitions)


def AutomatonConcat(a1: NFA, a2: NFA):
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
    
    return NFA(new_number_of_states, newq0, [newFinalState], newTransitions)


def AutomatonClosure(a1: NFA):
    
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
    
    return NFA(new_number_of_states, newq0, [newFinalState], newTransitions)





