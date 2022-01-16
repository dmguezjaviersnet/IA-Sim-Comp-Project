from Lexer import*

def test_lexer1():
    lex = Lexer([('+', Token_Type.plus),
    ('-', Token_Type.minus),
    ('\*', Token_Type.times),
    ('/', Token_Type.div),
    ('(1|2|3|4|5|6|7|8|9)(1|2|3|4|5|6|7|8|9)*', Token_Type.character),
    ('(\\ )*', Token_Type.space)],
     eof=Token_Type.eof)

    tokens = lex('1  + 22 * 3 -    16789')
    assert [token.lexeme for token in tokens] ==['1', '  ', '+', ' ', '22', ' ', '*', ' ', '3', ' ', '-', '    ', '16789', '$']
    assert [token.token_type for token in tokens] == [Token_Type.character, Token_Type.space, Token_Type.plus, Token_Type.space, Token_Type.character, Token_Type.space, Token_Type.times, Token_Type.space, Token_Type.character, Token_Type.space, Token_Type.minus, Token_Type.space, Token_Type.character, Token_Type.eof]


