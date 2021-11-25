from typing import Dict, List, Set


EPSILON = ''

class State:

    def __init__(self, id: int, tag: str, isFinal: bool = False):
        self.id = id
        self.tag = tag
        self.isFinal = isFinal

    def __str__(self) -> str:
        return f"Id:{self.id}\n Tag:{self.tag} \n isFinal:{self.isFinal}"

class Automaton:
    @property
    def number_of_states(self):
        return len(self.states)

    def __init__(self, nStates: int, q0:int , finalStates:List[int], transitions, statesList=[]):
        
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

        self.vocabulary.discard(EPSILON) # remove epsilon from vacabulary 
        

class NFA(Automaton):

    def __init__ (self, nStates, q0, finalStates, transitions, statesList = []):
        super().__init__(nStates, q0, finalStates, transitions, statesList)
    
    def epsilonTransitions(self, state):
        print(self.transitions.keys())
        if state in self.transitions.keys() and EPSILON in self.transitions[state].keys(): 
            return self.transitions[state][EPSILON]
        else:
            return []
    

    def __str__(self) -> str:
        return f" Number of States:{self.number_of_states}\n q0:{self.q0}\nTransitions:{self.transitions}\n finalStates={self.finals}"



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

#  Dado un conjunto de estados y un simbolo yo voy a obtener el conjunto de estados a los cuales yo 
# llego si parto de los estados iniciales
def goTo(automaton:'NFA', states: List[int], symbol: str):
    goto = set()

    for state in states:
        if state in automaton.transitions.keys() and symbol in automaton.transitions[state].keys():
            goto.update(automaton.transitions[state][symbol])
    
    return goto


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
              
                    
                if current.id not in transitions.keys(): 
                    transitions[current.id] = {}
                if  symbol in transitions[current.id].keys():
                    Exception('not DFA from NFA')
                else:
                    transitions[current.id][symbol] = qi.id

                if qi not in statesforDFA:
                    stack.append(qi)
                    statesforDFA.append(qi)
    
    finals = [ s.id for s in statesforDFA if s.isFinal]
    
    statesList = [State(i.id, i.tag, i.isFinal) for i in statesforDFA]

    return DFA(nStates = len(statesforDFA), q0 = 0, finalStates = finals, transitions = transitions, statesList = statesList)

    
    


class DFA(Automaton):


    def __init__(self, nStates: int, q0: int, finalStates: List[int],  transitions, statesList = []):
        
        temp: Dict = {}
        for i, j in transitions.items():
            for k,l in j.items():
                temp[(i,k)] = l
        
        
        super().__init__(nStates, q0, finalStates, temp, statesList)
    

    def __str__(self) -> str:
        return f"States: {self.states}\n q0:{self.q0} \n Final States: {self.finals} \n Transitions: {self.transitions} \n Vocabulary: {self.vocabulary} "

    

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
    

def AutomatonUnion(a1: Automaton, a2: Automaton):

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
        if (fs, EPSILON) not in a1.transitions.keys():
            newTransitions[(fs+newa1start, EPSILON)] = [newFinalState]
        else:
            newTransitions[(fs+newa1start, EPSILON)].append(newFinalState)
    
    for fs in a2.finals:
       if (fs, EPSILON) not in a2.transitions.keys():
           newTransitions[(fs+newa2start, EPSILON)] = [newFinalState]
       else:
           newTransitions[(fs+newa2start, EPSILON)].append(newFinalState)

    new_number_of_states = a1.number_of_states + a2.number_of_states + 2
    
    return NFA(new_number_of_states, newq0, [newFinalState], newTransitions)





