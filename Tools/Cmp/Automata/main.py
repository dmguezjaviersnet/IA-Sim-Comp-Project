
from automaton import *
import pytest
from astRegex import *

def main():
    nfa = NFA( nStates =4, q0 = 0,finalStates=[3], transitions={
    (0, EPSILON): [ 1],
    (0, 'a'):[0],
    (0, 'b') : [0],
    (1, 'a'): [ 2 ],
    (2,'a'):  [ 3 ],
    (2,'b'):  [ 3 ]
})
    # print(nfa.number_of_states)
    # print(nfa.transitions)
    # print(epsilonClosure(nfa, [0]))
    # print(goTo(nfa,[2] , 'a'))
    # dfa = NFAtoDFA(nfa)
    # print(nfa)
    # print(dfa)

    # for i in dfa.states:
    #     print(i)
    # for i in nfa.states:
    #     print(i)
    # print(dfa.number_of_states)
    # test_union()
    test_closure()
    #test_concat()
    # test_ast()

def test_ast():
    concat  = ConcatNode(SymbolNode('a'), SymbolNode('b'))
    x1 = concat.eval()
    union = UnionNode(SymbolNode('1'), SymbolNode('g'))
    x2 = union.eval()
    closure = ClosureNode(SymbolNode('p'))
    x3 = closure.eval()
    print(x1)
    print(x2)
    print(x3)


def test_concat():
    
    a1 = NFA(2, 0, [1], {
        (0,'a') : [1]
    })

    a2 = NFA(2, 0, [1], {
        (0,'b') : [1]
    })

    concat = AutomatonConcat(a1, a2)

    print(concat)

    match = NFAtoDFA(concat).match

    print(match('b'))
    print(match('a'))
    print(match('aa'))
    print(match('ab'))

def test_union():
    a1 = NFA(2, 0, [1], {
        (0,'a') : [1]
    })

    a2 = NFA(2, 0, [1], {
        (0,'b') : [1]
    })

    union = AutomatonUnion(a1, a2)

    print(union)

    match = NFAtoDFA(union).match

    print(match('b'))
    print(match('a'))
    print(match('aa'))
    print(match('abb'))

def test_closure():
    a1 = NFA(2, 0, [1], {
        (0,'a') : [1]
    })

    a2 = NFA(2, 0, [1], {
        (0,'b') : [1]
    })

    "(a|b)*"
    closure = AutomatonClosure(AutomatonUnion(a1, a2))

    print(closure)

    match = NFAtoDFA(closure).match

    print(match(''))
    print(match('b'))
    print(match('a'))
    print(match('aa'))
    print(match('ab'))
    print(match('aaaaaa'))
    print(match('c'))


if __name__ == '__main__':
    main()