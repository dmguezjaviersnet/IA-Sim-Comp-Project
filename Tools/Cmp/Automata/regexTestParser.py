# Regex Grammatica
# E -> T 
#    | '|' T E
# T -> F 
#    | F T
# F -> Atom | Atom SpecialChar
# Atom -> Char
#        | '(' Expr ')'
# Char -> AnyCharExceptEspecial | '\' AnyChar
# SpecialChar   -> '?' 
#               | '*' 
#               | '+'

from typing import List


pattern: str = '';
pos: int = 0;

peek = lambda  : pattern[pos]
hasMoreChars =  lambda : pos < len(pattern)

isSpecialChar = lambda ch : ch == '*' or ch == '+' or ch == '?'


class NodeTree:

    def __init__(self, symbol: str, children: List['NodeTree'] = []):
        self.symbol = symbol
        self.children = children

def match(symbol: str):
    if peek() != symbol:
        assert(f"Unexpected symbol {peek()} ")
    global pos
    pos += 1

def next():
    symbol = peek()
    match(symbol)
    return symbol


def E():
    t = T()
    if hasMoreChars() and peek() == '|':
        match('|')
        e = E()
        return NodeTree('E', [t, NodeTree('|'), e])
    return NodeTree('E', [t])

    

def T (): 
    f = F()
    if hasMoreChars() and peek() != ')' and peek() != '|':
        t = T()
        return NodeTree('T', [f, t])
    
    return NodeTree('T', [f])

def F():
    atom = Atom()
    if hasMoreChars() and isSpecialChar(peek()):
        special = next()
        return NodeTree('F', [atom, NodeTree(special)])
    return NodeTree('F', [atom])


def Atom():
    if peek() == '(':
        match('(')
        exp = E()
        match(')')
        return NodeTree('Atom', [NodeTree('('), exp, NodeTree(')')])
    return NodeTree('Atom', [Char()])    

def Char():
    if isSpecialChar(peek()):
        assert("")
    if peek() == '\\':
        match('\\')
        return NodeTree('Char', [NodeTree('\\'), NodeTree(next())])
    return NodeTree('Char',[NodeTree(next())])

def toParseTree(regex: str):
    regex = regex.replace(" ", "")
    print(regex)
    global pattern
    pattern = regex
    global pos
    pos = 0
    return E()
    

# def main():
   

# main()