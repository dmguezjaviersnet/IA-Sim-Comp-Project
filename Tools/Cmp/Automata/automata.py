from typing import Dict, List, Set

from regexTestParser import *




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
            elif token == '?':
                stack.append(NFA.zeroOrOne(stack.pop()))
            elif token == '+':
                stack.append(NFA.oneOrMore(stack.pop()))
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
# 
    @staticmethod
    def zeroOrOne(nfa: 'NFA'):
        start = NFA.createState(False)
        end = NFA.createState(False)

        NFA.addEpsilonTransition(start, end)
        NFA.addEpsilonTransition(start, nfa.start)

        NFA.addEpsilonTransition(nfa.end, end)
        nfa.end.isEnd = False

        return NFA(start, end)

    @staticmethod
    def oneOrMore(nfa: 'NFA'):
        start = NFA.createState(False)
        end = NFA.createState(True)

        NFA.addEpsilonTransition(nfa, nfa.start)
        NFA.addEpsilonTransition(nfa.end, end)
        NFA.addEpsilonTransition(nfa.end, nfa.start)
        nfa.end.isEnd = False

        return NFA(start, end)
        

    @staticmethod
    def addNextState(state: 'State', nextStates: List['State'], visited)-> None:
        if len(state.epsilonTransitions):
            for st in state.epsilonTransitions:
                if not any( vs == st for vs in visited):
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
                if symbol in state.transitions.keys():
                    nextState = state.transitions[symbol]
                    NFA.addNextState(nextState, nextStates, [])
                
                    
            currentStates = nextStates
    
        return any ( state.isEnd for state in  currentStates)

    @staticmethod
    def createMatcher(exp: str):
        ast = toParseTree(exp)
        nfa = NFA.toNFAfromAST(ast)
        return lambda word: NFA.search(nfa, word)
    
    @staticmethod
    def toNFAfromAST(ast: NodeTree)-> 'NFA':
        if ast.symbol == 'E':
            t = NFA.toNFAfromAST(ast.children[0])
            if len(ast.children) == 3: # E -> T | E 
                return NFA.union(t, NFA.toNFAfromAST(ast.children[2]))
            return t
        if ast.symbol == 'T':
            f = NFA.toNFAfromAST(ast.children[0])
            if len(ast.children) == 2: # T -> F  T
                return NFA.concat(f, NFA.toNFAfromAST(ast.children[1]))
            return f
        if ast.symbol == 'F':
            atom = NFA.toNFAfromAST(ast.children[0])
            if len(ast.children) == 2: # F -> Atom SpecialCharacter
                special = ast.children[1].symbol
                if special == '*':
                    return NFA.closure(atom)
                if special == '+':
                    return NFA.oneOrMore(atom)
                if special == '?':
                    return NFA.zeroOrOne(atom)
            return atom # F-> Atom
        if ast.symbol == 'Atom':
            if len(ast.children) == 3: # Atom -> (E)
                return NFA.toNFAfromAST(ast.children[1])
            return NFA.toNFAfromAST(ast.children[0])
        if ast.symbol == 'Char':
            if len(ast.children) == 2: # Char-> '\' AnyCharacter
                return NFA.fromSymbol(ast.children[1].symbol)
            return NFA.fromSymbol(ast.children[0].symbol) # Char-> AnyCharNotEspecial
        assert(f'Unrecognized symbol {ast.symbol}') 
    
