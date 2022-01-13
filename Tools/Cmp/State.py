
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
                goTo = goTo2(symbol, *eClosure)
                eClosure = epsilonClosure2(*goTo)

                if eClosure not in eClosures:
                    newState = State(tuple(eClosure), any(state.isFinal for state in eClosure))
                    eClosures.append(eClosure)
                    states.append(newState)
                    stack_pending.append(newState)
                
                else:
                    newState = states[eClosures.index(eClosure)]
                
                currentState.add_transition(symbol, newState)

        return q0          


        
        
    


        

    
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

