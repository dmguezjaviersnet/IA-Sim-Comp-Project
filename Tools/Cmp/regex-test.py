from cmp_main_test import *




def testregex1():
    tokens = regexTokenizer('a|ε')
    ast, _= non_recursive_parse(regex_grammar, tokens)
    nfa = ast.eval()
    dfa = NFAtoDFA(nfa)
    assert dfa.match('a') == True
    assert dfa.match('ab') == False
    assert dfa.match('ac') == False
    assert dfa.match('') == True
    assert dfa.match('bc') == False


def testregex2():
    tokens = regexTokenizer('(a|b)*')
    ast, _= non_recursive_parse(regex_grammar, tokens)
    nfa = ast.eval()
    dfa = NFAtoDFA(nfa)
    a = dfa.match('aa') == True
    print(a)
    # assert a == True
    # assert dfa.match('ccc') == True
    # assert dfa.match('') == True
    # assert dfa.match('abc') == True


# testregex2()