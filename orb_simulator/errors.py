class OrbisimSemanticError(Exception):
    @property 
    def error_info(self):
        return self.args[0]
class OrbisimExecutionError(Exception):
    @property 
    def error_info(self):
        return self.args[0]

class OrbisimLexerError(Exception):
    @property 
    def error_info(self):
        return self.args[0]
    @property
    def lexeme(self):
        return self.args[1]
class OrbisimParserError(Exception):
    @property 
    def error_info(self):
        return self.args[0]