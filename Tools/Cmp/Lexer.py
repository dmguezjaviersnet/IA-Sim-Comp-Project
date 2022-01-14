from State import*
from typing import Tuple
from Own_token import Token
from State import *
from Regex_Engine import *

class Lexer:

    def __init__(self, regex_table: Tuple[str, Token_Type], eof) -> None:
        self.regexs =  self._build_regex_automatons(regex_table)
        self.eof = eof
        self.automaton = self._build_automaton()

    
    def _build_automaton(self):
        start = State('initial_state')

        for state in self.regexs:
            start.add_epsilon_transition(state)
        
        return start.to_DFA()
        
    def _build_regex_automatons(self, regex_table: Tuple[str, Token_Type]):
        regex_automatons = []

        for priority, (regex, token_type) in enumerate(regex_table):

            automaton, states = State.from_old_model_to_new_model(Regex_Engine(regex).automaton, True)

            for state in states:
                if state.is_final_state:
                    state.tag = (priority, token_type)
            
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

        return  endState if endState else None
    
    def _tokenizer(self, text):

        while text:
            qf = self._walk(text)
            lexeme = qf.lexeme

            if qf == None:
                pass # exception :(
            
            text = text[len(lexeme):]
            ends = [state.tag for state in qf.substates if state.tag]
            ends.sort()

            yield lexeme, ends[0][1]

        yield '$', self.eof

    def __call__(self, text):
        return [Token(lexeme, token_type) for lexeme, token_type in self._tokenizer(text)]
    
