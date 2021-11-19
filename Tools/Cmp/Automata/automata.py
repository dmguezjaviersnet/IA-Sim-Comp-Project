from typing import Dict, List, Set




class State:

    def __init__(self, isEnd: bool):
        self.isEnd = isEnd
        self.epsilonTransitions: Set[State] = set()
        self.transitions: Dict[str, List[State]]  = {}
    
    
class NFA:


    def __init__(self, start: 'State', end: 'State') -> None:
        self.start: 'State' = start
        self.end: 'State' = end
    # def match():...

    @staticmethod
    def createState(isEnd)-> 'State':
        return State(isEnd)
    
    # def addTransition():...

    @staticmethod
    def addEpsilonTransition(fromState: 'State', toState: 'State')-> None:
        fromState.epsilonTransitions.add(toState)
    
    @staticmethod
    def addTransition(fromState: 'State' , toState: 'State', symbol: str)-> None:
        fromState.transitions[symbol] = toState
        
    
    @staticmethod
    def fromEpsilon()-> 'NFA':
        start = NFA.createState(False)
        end = NFA.createState(True)
        NFA.addEpsilonTransition(start, end)
        return NFA(start, end)


    @staticmethod
    def fromSymbol(symbol: str)-> 'NFA':
        start = NFA.createState(False)
        end = NFA.createState(True)
        NFA.addTransition(start, end, symbol)
        return NFA(start, end)
    
    @staticmethod
    def concat(first: 'NFA', second: 'NFA'):
        NFA.addEpsilonTransition(first.end, second.start)
        first.end.isEnd = False
        return NFA(first.start, second.end)
    
    @staticmethod
    def union(first: 'NFA', second: 'NFA'):
       start = NFA.createState(False)
       NFA.addEpsilonTransition(start, first.start)
       NFA.addEpsilonTransition(start, second.start)

       end = NFA.createState(True)
       NFA.addEpsilonTransition(first.end, end)
       first.end.isEnd = False
       NFA.addEpsilonTransition(second.end, end)
       second.end.isEnd = False
       return NFA(start=start, end = end)
    
    @staticmethod
    def closure(nfa: 'NFA')-> 'NFA':
        start = NFA.createState(False)
        end = NFA.createState(True)

        NFA.addEpsilonTransition(start, end)
        NFA.addEpsilonTransition(start, nfa.start)
        NFA.addEpsilonTransition(nfa.end, end)
        NFA.addEpsilonTransition(nfa.end, nfa.start)
        nfa.end.isEnd = False

        return NFA(start= start, end = end)

    @staticmethod
    def toNFA(postfixExp)-> 'NFA':
        if postfixExp == '':
            return NFA.fromEpsilon()

        stack = []

        for token in postfixExp:
            if token == '*':
                stack.append(NFA.closure(stack.pop()))
            elif token == '|':
                right = stack.pop()
                left = stack.pop()
                stack.append(NFA.union(left, right))
            elif token == '.':
                right = stack.pop()
                left = stack.pop()
                stack.append(NFA.concat(left, right))
            else:
                stack.append(NFA.fromSymbol(token))
        
        nfa = stack.pop()
        return nfa

    def zeroOrOne(nfa: 'NFA'):
        start = NFA.createState(False)
        end = NFA.createState(False)

        NFA.addEpsilonTransition(start, end)
        NFA.addEpsilonTransition(start, nfa.start)

        NFA.addEpsilonTransition(nfa.end, end)
        nfa.end.isEnd = False

        return NFA(start, end)

    def zeroOrMore(nfa):
        

    @staticmethod
    def addNextState(state: 'State', nextStates: List['State'], visited)-> None:
        if len(state.epsilonTransitions):
            for st in state.epsilonTransitions:
                if not visited.find(lambda vs: vs == st):
                    visited.append(st)
                    NFA.addNextState(st, nextStates, visited)
        else:
            nextStates.append(state)
    
    @staticmethod
    def search(nfa: 'NFA', word: str):
        currentStates: List['State'] = []
        NFA.addNextState(nfa.start, currentStates, [])

        for symbol in word:
            nextStates = []

            for state in currentStates:
                nextState = state.transitions[symbol]
                if nextState:
                    NFA.addNextState(nextState, nextStates, [])
            currentStates = nextStates
    
        return any ( state.isEnd for state in  currentStates)

    @staticmethod
    def createMatcher(exp: str):
        nfa = NFA.toNFA(exp)
        return lambda word: NFA.search(nfa, word)