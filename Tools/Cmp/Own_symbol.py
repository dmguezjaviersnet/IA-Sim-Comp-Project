from typing import overload


class Symbol:
    """docstring for Symbol."""
    def __init__(self, id: str, *args):
        self.identifier = id
        self.attrs = []

        for elem in args:
            setattr(self, elem, None)
            self.attrs.append(elem)
            