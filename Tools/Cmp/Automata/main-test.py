from automata import *
from regexTestParser import *

def main():
    regex = ('((a)      (b)     |       c) *')
    match = NFA.createMatcher(regex)

    print(match(''))
    print(match('a'))
    print(match('b'))
    print(match('ab'))
    print(match('c'))
    print(match('abcccab'))
    print(match('acca'))

if __name__ == '__main__':
    main()