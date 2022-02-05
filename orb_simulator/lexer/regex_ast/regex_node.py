from abc import abstractmethod

class Node:

    '''Objeto para representar nodos de AST para REGEX'''

    @abstractmethod
    def eval(self):
        ...