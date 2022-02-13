from lexer.regex_engine import Regex_Engine
from parser.own_token import Token_Type
from automaton.automaton import Automaton
from automaton.state import State

def test_regex_engine1():
    regexengine = Regex_Engine('(a|b|c)*')
    automaton = regexengine.automaton
    automaton = State.from_old_model_to_new_model(automaton)
    assert automaton.match_from_nfa('aaab') == True
    assert automaton.match_from_nfa('bbb') == True
    assert automaton.match_from_nfa('') == True
    assert automaton.match_from_nfa('abcd') == False

def test_regex_engine2():
    regexengine = Regex_Engine('(a|b|c)*')
    automaton = regexengine.automaton
    automaton = State.from_old_model_to_new_model(automaton)
    automaton = automaton.to_DFA()
    assert automaton.match_from_dfa('aaab') == True
    assert automaton.match_from_dfa('bbb') == True
    assert automaton.match_from_dfa('') == True
    assert automaton.match_from_dfa('aaef') == False

def test_regex_engine3_check_type():
    regexengine = Regex_Engine('(a|b|c)*')
    automaton = regexengine.automaton
    assert type(regexengine) is Regex_Engine
    assert type(automaton) is Automaton

def test_tokenizer_regex1():
    tokens = Regex_Engine.regex_tokenize('(a|b)*')
    assert [token.lexeme for token in tokens] == ['(', 'a', '|', 'b', ')', '*', '$']
    assert [token.token_type for token in tokens] == [Token_Type.open_parenthesis, Token_Type.character, Token_Type.union, Token_Type.character, Token_Type.closed_parenthesis, Token_Type.closure, Token_Type.eof]
    