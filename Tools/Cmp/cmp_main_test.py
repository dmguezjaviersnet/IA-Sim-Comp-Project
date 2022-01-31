from regex_grammar import regex_grammar
from arth_grammar import arth_grammar, arth_grammar_tokenize, arth_grammar_token_string
from test_grammar_lr1 import lr1_test_grammar, test_grammar_tokenize
from regex_engine import Regex_Engine
from lexer import Lexer
from own_token import Token_Type, Token
from state import State
from lr1_parser import lr1_parse
from orbsim_grammar import simorb_grammar, simorb_token_string
from orbsim_lexer import orbsim_lexer

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
    ('\-', Token_Type.minus),
    ('\*', Token_Type.times),
    ('/', Token_Type.div),
    ('\(', Token_Type.open_parenthesis),
    ('\)', Token_Type.closed_parenthesis),
    ('[0-9]+', Token_Type.character),
    ('(\\ )*', Token_Type.space)],
     eof=Token_Type.eof)

    tokens = lex('(3+5)*(4/(5-8)')
    success, ast = lr1_parse(arth_grammar, tokens)
    
    for i in tokens:
        print(i)
    print(':)')
    

def main():
    ############################### Gramática de Regex #################################
    # re = Regex_Engine('(a|b)*')
    
    # au = re.automaton
    # test_lexer()
    # test_lexer()
    
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

    ############################### Probando parser LR(1) ##############################


    # Testeo Hashing
    # item1 = Lr1_item(Lr0_item(Non_terminal('P'), (Terminal('b'), Non_terminal('X')), 0), frozenset({'$'}))
    # item2 = Lr1_item(Lr0_item(Non_terminal('E'), (Terminal('b'), Non_terminal('X')), 0), frozenset({'$'}))

    # item3 = Lr1_item(Lr0_item(Non_terminal('P'), (Terminal('b'), Non_terminal('X')), 0), frozenset({'$'}))
    # item4 = Lr1_item(Lr0_item(Non_terminal('E'), (Terminal('b'), Non_terminal('X')), 0), frozenset({'$'}))

    # tup1 = (item1, item2)
    # tup2 = (item3, item4)

    # print(item1 == item2)
    # print(hash(item1) == hash(item3))

    # print(hash(tup1) == hash(tup2))

    tokens = orbsim_lexer('''func Sum(a, b) {
        let c = a+b;
        
        if (!a+b)
            then ret false;
        
        ret true;
        }'''
    )

    lr1_parse(simorb_grammar, tokens, simorb_token_string)

    # a = (1, 2)
    # b = (2, 1)
    # print(hash(a) == hash(b))

if __name__ == '__main__':
    main()