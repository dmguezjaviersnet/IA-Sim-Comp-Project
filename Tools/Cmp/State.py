
from automaton import *

class State:
    
    '''
        Automaton representation with State
    '''

    def __init__(self, id , isFinal: bool = False, substates:Tuple['State'] = ()):
        self.id = id
        self.tag = None
        self.substates: Tuple['State'] = substates
        self.isFinal: bool = isFinal
        self.transitions: Dict[str, 'State']= {}
        self.epsilon_transitions: Set['State']  = set()
    
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

    
    

    @property
    def e_closure(self):
        return State.epsilon_closure([self])
    
    @property
    def name(self):
        return str(self.id)
    
    @property
    def symbols(self):
        symbols = set()
        
        for substate in self.substates:
            for symbol in substate.transitions:
                symbols.add(symbol)
        return symbols
        
    @staticmethod
    def epsilon_closure(states: 'State'): # model with State
        '''
        
        '''
        eClosure = set(states)
        stack = list(states)

        while len(stack):
            state = stack.pop()
            for eTransition in state.epsilon_transitions:
                if not eTransition in eClosure:
                    stack.append(eTransition)
                    eClosure.add(eTransition)

        return eClosure


    @staticmethod
    def go_to(symbol: str, states: 'State'):
        goto = set()

        for state in states:
            if state.has_a_transition(symbol):
                for s in state[symbol]:
                    goto.add(s)

        return goto

    def to_DFA(self):
        e_closure: Set[State] = self.e_closure
        initial_state: 'State' = State(tuple(e_closure), any(state.isFinal for state in e_closure), tuple(e_closure))

        e_closures = [e_closure]
        states = [initial_state]
        stack_pending_states: List['State'] = [initial_state] 

        while len(stack_pending_states):
            currentState: 'State' = stack_pending_states.pop()
            symbols: Set['State'] = currentState.symbols
            
            
            for symbol in symbols:
                go_to = State.go_to(symbol, currentState.substates)
                e_closure = State.epsilon_closure(go_to)

                if e_closure not in e_closures:
                    new_state = State(tuple(e_closure), any(state.isFinal for state in e_closure), tuple(e_closure))
                    e_closures.append(e_closure)
                    states.append(new_state)
                    stack_pending_states.append(new_state)
                
                else:
                    new_state = states[e_closures.index(e_closure)]
                
                currentState.add_transition(symbol, new_state)

        return initial_state          


    @staticmethod
    def from_old_model_to_new_model(automaton: 'Automaton', returnStatesList=False):
        states = []

        for n in range(automaton.number_of_states):
            state = State(f"q{n}", n in automaton.finals)
            states.append(state)

        for origin, t  in automaton.transitions.items():
            
            origin = states[origin]
            
            for symbol, dest in t.items():
                
                origin[symbol] = [ states[d] for d in dest]
                
        
        return states[0] if returnStatesList else states[0], states

    


        

    
    def __str__(self) -> str:
        return f"Id:{self.id}\n Tag:{self.tag} \n isFinal:{self.isFinal}"
    
    def __setitem__(self, symbol, value):
        if symbol == EPSILON:
            self.epsilon_transitions = value
        else:
            self.transitions[symbol] = value
    
    def __getitem__(self, symbol: str):
        if symbol == EPSILON:
            return self.epsilon_transitions
        try:
            return self.transitions[symbol]
        except KeyError:
            return None 

