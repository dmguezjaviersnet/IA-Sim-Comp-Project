from typing import Dict, List, Set


class State:

    def __init__(self, state, final):
        self.final = final
        self.epsilonTransitions: Set[State] = {}
        self.transitions: Dict[str, List[State]]  = set()
    
    def match():...

    def addState():...
    
    def addTransition():...

    def addEpsilonTransition():...

    
