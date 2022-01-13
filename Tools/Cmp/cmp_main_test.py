
from Regex_Engine import Regex_Engine
from nonr_parser import non_recursive_parse
from automaton_tools import NFAtoDFA
from regex_grammar import regex_grammar

def main():
    ############################### Gramática de Regex #################################
    re = Regex_Engine('(a|ε)*')
    

    
    # print(parsed2)
    # nfa = ast.eval()
    # dfa = NFAtoDFA(nfa)
    # print(dfa.match('aaaaa'))
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

