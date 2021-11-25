class Token:
    def __init__(self, line, column, type, lexeme):
      self.line = line
      self.column = column
      self.type = type
      self.lexeme = lexeme