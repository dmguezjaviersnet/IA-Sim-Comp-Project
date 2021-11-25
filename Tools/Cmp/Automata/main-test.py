from automata import *
from regexTestParser import *

def main():
    regex = ('(\\)*')
    match = NFA.createMatcher(regex)

    print(match('\\'))
    # print(match('a'))
    # print(match('b'))
    # print(match('ab1'))
    # print(match('c'))
    # print(match('abcccaba'))
    # print(match('acca'))
    

if __name__ == '__main__':
    main()