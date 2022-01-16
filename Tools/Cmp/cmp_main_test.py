
from Regex_Engine import Regex_Engine
from Lexer import Lexer
from Own_token import Token_Type, Token
from Terminal import EOF
from nonr_parser import non_recursive_parse
from regex_grammar import regex_grammar
from State import*


def test1():
    regexengine = Regex_Engine('(a|b|c)?')
    automaton = regexengine.automaton
    automaton = State.from_old_model_to_new_model(automaton)
    automaton = automaton.to_DFA()
    print(automaton.match_from_dfa('aa'))
    # assert automaton.match_from_dfa('bbb') == True
    # assert automaton.match_from_dfa('') == True
    # assert automaton.match_from_dfa('aaef') == False
    
    

def test_lexer():
    lex = Lexer([('\+', Token_Type.plus),
    ('-', Token_Type.minus),
    ('\*', Token_Type.times),
    ('/', Token_Type.div),
    ('\(', Token_Type.open_parenthesis),
    ('\)', Token_Type.closed_parenthesis),
    ('(1|2|3|4|5|6|7|8|9)+', Token_Type.number),
    ('(\\ )*', Token_Type.space)],
     eof=Token_Type.eof)

    tokens = lex('( 1+22*3) -           16789')
    
    for i in tokens:
        print(i)
    print(':)')
    

def main():
    ############################### Gramática de Regex #################################
    # re = Regex_Engine('(a|b)*')
    
    # au = re.automaton
    # test_lexer()
    test_lexer()
    
    # tokens = Regex_Engine.regexTokenizer('(a|b)*')
    # a1 = [t.token_type for t in tokens]
    # a2 = [t.lexeme for t in tokens]
    # print(a1)
    # print(a2)
    # for i in tokens:
    #     print(i)
    # test_lexer()
    # # print(parsed2)
    # # nfa = ast.eval()
    # # dfa = NFAtoDFA(nfa)
    # print(au.match('aaaaa'))
    # print(au.match('aaaaab'))
    # print(au.match(''))
    # print(au.match('ababbb'))
    # print(au.match('ababbb'))
    # print(dfa.match('abbbbed'))
    # print(dfa.match('aaed'))
    # print(dfa.match('ed'))
    # print(dfa.match('aaaaabbbbaaed'))
    # print(dfa.match('aaaaabbbba'))
    # print(dfa.match(''))

    # print('finished \n\n')
    # print(regex_grammar)
    # print(parsed2)
    # print(parsed)

    ############################### Gramática de prueba (aritmética) #################################

if __name__ == '__main__':
    main()

