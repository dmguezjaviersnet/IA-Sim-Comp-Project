
from automaton import *

class State:
    
    '''
        Con esta clase se representa un estado del autómata,
        partiendo del State inicial se puede recorrer todo el autómata
        por lo que vasta con tener el estado inicial representado con State
        para tener una representación de todo el autómata
    '''

    def __init__(self, id , is_final_state: bool = False, substates:Tuple['State'] = ()):
        self.id = id
        self.tag = None
        self.substates: Tuple['State'] = substates
        self.is_final_state: bool = is_final_state
        self.transitions: Dict[str, 'State']= {}
        self.epsilon_transitions: Set['State']  = set()
    
    def has_a_transition(self, symbol):
        '''
            Dice si con este estado y el símbolo de entrada <symbol> existe 
            alguna transición 
        '''
        return symbol in self.transitions.keys()
    
    def add_transition(self, symbol: str, state: 'State'):
        '''
            Dado un símbolo<symbol> y un estado <state> agrega una transición
            del estado en donde estas <self> con el símbolo <symbol> al estado 
            <tates>
        '''
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
    
    @staticmethod
    def get_symbols_from_states(states):
        '''
            Devuelve el conjunto de símbolos de todos los subestados que contiene un estado de un DFA
        '''
        symbols = set()
        for state in states:
            for symbol in state.transitions:
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

    def to_DFA(self) -> 'State':
        '''
            Convierte un NFA(Automáta Finito No Determinista) a un DFA(Automáta Finito Determinista)
        '''
        e_closure: Set[State] = self.e_closure # epsilon clausura del estado inicial 
        index = 0 
        initial_state: 'State' = State(f'q_{index}', any(state.is_final_state for state in e_closure), tuple(e_closure)) # estado inicial
        index +=1
        e_closures = [e_closure] # lista que va a ir guardando las epsilon clausuras que han sido calculadas
        states = [initial_state] # lista que va a ir guardando todos los estados del autómata
        stack_pending_states: List['State'] = [initial_state] # pila que va a tener los estados que faltan por sacar

        while len(stack_pending_states): # mientras queden elementos por sacar de la pila
            currentState: 'State' = stack_pending_states.pop() # saca el próximo estado
            symbols: Set['State'] = State.get_symbols_from_states(currentState.substates) # 
            
            
            for symbol in symbols: # ve por cada símbolo 
                go_to = State.go_to(symbol, currentState.substates) # calculo el goto 
                e_closure = State.epsilon_closure(go_to) # calculo la epsilon clausura al resultado del goto

                if e_closure not in e_closures: # compruebo que esa epsilon clausura no la haya tenido previamente
                    new_state = State(f'q_{index}', any(state.is_final_state for state in e_closure), tuple(e_closure))
                    index += 1 
                    e_closures.append(e_closure)
                    states.append(new_state)
                    stack_pending_states.append(new_state)
                
                else:
                    new_state = states[e_closures.index(e_closure)]
                
                currentState.add_transition(symbol, new_state)

        return initial_state          


    @staticmethod
    def from_old_model_to_new_model(automaton: 'Automaton', returnStatesList=False):
        '''
            Lleva del modelo con la clase Automaton al modelo solo con states más 
            conveniente para poder agregar propiedades a los estados.
        '''
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
        return f"Id:{self.id}\n Tag:{self.tag} \n isFinal:{self.is_final_state}"
    
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

