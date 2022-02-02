class OrbisimSemanticError(Exception):
    @property 
    def error_info(self):
        return self.args[0]

class OrbisimLexerError(Exception):
    @property 
    def error_info(self):
        return self.args[0]

class OrbisimParserError(Exception):
    @property 
    def error_info(self):
        return self.args[0]