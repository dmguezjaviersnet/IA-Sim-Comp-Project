from Regex_Engine import Regex_Engine
from State import*

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

