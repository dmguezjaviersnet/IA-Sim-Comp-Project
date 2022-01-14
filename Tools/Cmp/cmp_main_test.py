
from Regex_Engine import Regex_Engine
from Lexer import Lexer
from Own_token import Token_Type, Token
from Terminal import EOF
from nonr_parser import non_recursive_parse
from automaton_tools import NFAtoDFA
from regex_grammar import regex_grammar


def main():
    ############################### Gramática de Regex #################################
    # re = Regex_Engine('(a|b)*')
    # au = re.automaton
    lex = Lexer([('+', Token_Type.plus),
    ('-', Token_Type.minus),
    ('\*', Token_Type.times),
    ('/', Token_Type.div),
    ('(1|2|3|4|5|6|7|8|9)(1|2|3|4|5|6|7|8|9)*', Token_Type.character)],
     eof=Token('$', Token_Type.eof))

    tokens = lex('1+22*3')
    for i in tokens:
        print(i)
    print(':)')
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

