from typing import List
from State import State
from automaton import NFA, DFA, Automaton, StatesContainer

EPSILON = ''

'''
Model with State
'''
def epsilonClosure2(*states: 'State'): # model with State
    eClosure = set(states)
    stack = list(states)
    
    while len(stack):
        state = stack.pop()
        for eTransition in state.epsilon_transitions:
            if not eTransition in eClosure:
                stack.append(eTransition)
                eClosure.add(eTransition)
    
    return eClosure

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
'''
Model with State
'''
def goTo2(symbol: str, *states: 'State'):
    goto = set()

    for state in states:
        if state.has_a_transition(symbol):
            goto.update(state[symbol])
    
    return goto

def goTo(automaton:'NFA', states: List[int], symbol: str):
    goto = set()

    for state in states:
        if state in automaton.transitions and symbol in automaton.transitions[state]:
            goto.update(automaton.transitions[state][symbol])
    
    return goto

def from_old_model_to_new_model(automaton: 'Automaton', returnStatesList=False):
    states = []
    
    for n in range(automaton.states):
        state = State(f"q{n}", n in automaton.finals)
        states.append(state)
    
    for origin, t  in automaton.transitions.items():
        for symbol, dest in t.items():
            origin = states[origin]
            origin[symbol] = [ states[d] for d in dest]
    
    return states[0] if returnStatesList else states[0], states

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

# Operciones entre autómatas

def AutomatonUnion(a1: NFA, a2: NFA):
    '''
        Returns the union operation between two automatas
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