from automaton.state import State
from typing import List, Tuple
from parser.own_token import Token, Token_Type
from lexer.regex_engine import Regex_Engine
from errors import OrbisimLexerError

class Lexer:

    def __init__(self, regex_table: Tuple[str, Token_Type], eof) -> None:
        '''
            Se define una tabla de tokens<regex_table> 
            (conjunto de tuplas de la forma <regex, token_type>)
        '''
        self.regexs =  self._build_regex_automatons(regex_table)
        self.eof = eof 
        self.automaton = self._build_automaton()
        self.errors = List[str]

    
    def _build_automaton(self):
        start = State('initial_state')

        for state in self.regexs:
            start.add_epsilon_transition(state)
        
        return start.to_DFA()
        
    def _build_regex_automatons(self, regex_table: Tuple[str, Token_Type]):
        
        '''
        Al crear el automata queda dicho en cada estado final cuáles son los 
        tipos de tokens que se ven involucrados y cual es su prioridad, 
        dónde la prioridad se define en el orden en que se fue creando 
        la tabla de tal forma que los primeros son los que tienen más prioridad
        '''
        regex_automatons = []

        for priority, (regex, token_type) in enumerate(regex_table):

            automaton, states = State.from_old_model_to_new_model(Regex_Engine(regex).automaton, True)

            for state in states:
                if state.is_final_state:
                    state.tag = (priority, token_type) # por cada estado final del autómata que reconoce la expresión regular <regex> se agrega la tupla de (<priority>, <token_type>)
            
            regex_automatons.append(automaton)
        
        return regex_automatons


    def _walk(self, text):
        state = self.automaton
        endState = state if state.is_final_state else None
        lexeme = ''

        for symbol in text:
            if state.has_a_transition(symbol):
                lexeme += symbol
                state = state[symbol][0]

                if state.is_final_state:
                    endState = state
                    endState.lexeme = lexeme

            else:
              break
        
        if endState:
            return endState
        else:
            raise OrbisimLexerError('')
        return  endState if endState else None
    
    def _tokenizer(self, text):

        while text:
            qf = self._walk(text)
            

            if qf == None:
                
            
            else:
                lexeme = qf.lexeme
                text = text[len(lexeme):]
                ends = [state.tag for state in qf.substates if state.tag]
                ends.sort()
                yield lexeme, ends[0][1]

        yield '$', self.eof

    def __call__(self, text):
        return [Token(lexeme, token_type) for lexeme, token_type in self._tokenizer(text)]
    
