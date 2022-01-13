from Grammar import *
from Own_token import *
from nonr_parser import non_recursive_parse
from Terminal import *
from Non_terminal import *
from Production import *

from rules import *
from regex_rules import *

def main():
    ############################### Gramática de prueba (aritmética) #################################
    

    ############################### Gramática de Regex #################################


    tokens = regexTokenizer('(a|ε)*')
    ast, parsed2 = non_recursive_parse(regex_grammar, tokens)
    # print(parsed2)
    nfa = ast.eval()
    dfa = NFAtoDFA(nfa)
    print(dfa.match('aaaaa'))
    print(dfa.match('abbbbed'))
    print(dfa.match('aaed'))
    print(dfa.match('ed'))
    print(dfa.match('aaaaabbbbaaed'))
    print(dfa.match('aaaaabbbba'))
    print(dfa.match(''))

    print('finished \n\n')
    print(regex_grammar)
    # print(parsed2)
    # print(parsed)

if __name__ == '__main__':
    main()

