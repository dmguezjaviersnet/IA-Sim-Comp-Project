from automaton import *

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
    print(nfa)
    # print(dfa)

    # for i in dfa.states:
    #     print(i)
    # for i in nfa.states:
    #     print(i)
    # print(dfa.number_of_states)
    # test_union()


def test_union():
    a1 = NFA(2, 0, [1], {
        (0,'a') : [1]
    })

    a2 = NFA(2, 0, [1], {
        (0,'b') : [1]
    })

    union = AutomatonUnion(a1, a2)

    print(union)
    
if __name__ == '__main__':
    main()