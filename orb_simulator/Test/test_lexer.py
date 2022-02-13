from lexer import Lexer
from parser.own_token import Token_Type

def test_lexer():
    lex = Lexer([('\+', Token_Type.plus),
    ('\-', Token_Type.minus),
    ('\*', Token_Type.times),
    ('/', Token_Type.div),
    ('\(', Token_Type.open_parenthesis),
    ('\)', Token_Type.closed_parenthesis),
    ('([0-9])+', Token_Type.character),
    ('(\\ )*', Token_Type.space)],
     eof=Token_Type.eof)

    tokens = lex('(3 + 55  )*   (41 / (5 - 80 )')
    assert [token.lexeme for token in tokens] == ['(' ,'3', ' ', '+', ' ', '55', '  ', ')', '*', '   ', 
                                '(', '41', ' ', '/', ' ', '(', '5', ' ', '-', ' ', '80', ' ', ')', '$'
                                ]
    assert [token.token_type for token in tokens] == [Token_Type.open_parenthesis, Token_Type.character, Token_Type.space,
        Token_Type.plus, Token_Type.space, Token_Type.character, Token_Type.space, Token_Type.closed_parenthesis, Token_Type.times,
        Token_Type.space, Token_Type.open_parenthesis, Token_Type.character, Token_Type.space, Token_Type.div, Token_Type.space, 
        Token_Type.open_parenthesis, Token_Type.character, Token_Type.space, Token_Type.minus, Token_Type.space, Token_Type.character,
        Token_Type.space, Token_Type.closed_parenthesis, Token_Type.eof
        ]


