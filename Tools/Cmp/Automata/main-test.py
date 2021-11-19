from automata import *


def main():

    match = NFA.createMatcher('a*b')
    print(match(''))
    print(match('a'))
    print(match('b'))
    print(match('aab'))

if __name__ == '__main__':
    main()