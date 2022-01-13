
from automaton import *

class State:
    
    '''
        Automaton representation with State
    '''

    def __init__(self, id: str, isFinal: bool = False, substates:Tuple['State'] = ()):
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
    def eClosure(self):
        return epsilonClosure2(self)
    
    @property
    def name(self):
        return str(self.id)
    
    @property
    def symbols(self):
        symbols = set()
        
        for symbol in self.transitions.keys():
            symbol.add(symbol)
        
        return symbols
        
    @staticmethod
    def epsilon_closure(*states: 'State'): # model with State
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



    def go_to(symbol: str, *states: 'State'):
        goto = set()

        for state in states:
            if state.has_a_transition(symbol):
                goto.update(state[symbol])

        return goto

    def to_DFA(self):
        eClosure: Set[State] = self.eClosure
        q0: 'State' = State(''.join([state.id for state in eClosure]), any(state.isFinal for state in eClosure), tuple(eClosure))

        eClosures = list(eClosure)
        states = [q0]
        stack_pending: List['State'] = [q0] 

        while len(stack_pending):
            currentState: 'State' = stack_pending.pop()
            symbols: Set['State'] = set()
            
            for s in currentState.substates:
                symbols.union(s.symbols)

            for symbol in symbols:
                goTo = State.go_to(symbol, *eClosure)
                eClosure = State.epsilon_closure(*goTo)

                if eClosure not in eClosures:
                    newState = State(tuple(eClosure), any(state.isFinal for state in eClosure))
                    eClosures.append(eClosure)
                    states.append(newState)
                    stack_pending.append(newState)
                
                else:
                    newState = states[eClosures.index(eClosure)]
                
                currentState.add_transition(symbol, newState)

        return q0          


    @staticmethod
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

    


        

    
    def __str__(self) -> str:
        return f"Id:{self.id}\n Tag:{self.tag} \n isFinal:{self.isFinal}"
    
    def __setitem__(self, symbol, value):
        if symbol == EPSILON:
            self.epsilon_transitions.add(value)
        else:
            self.transitions[symbol] = value
    
    def __getitem__(self, symbol: str):
        if symbol == EPSILON:
            return self.epsilon_transitions
        try:
            return self.transitions[symbol]
        except KeyError:
            return None 

