from Lexer import Lexer
from Own_token import Token_Type

simorb_lexer = Lexer([
    ('\+', Token_Type.plus),
    ('\-', Token_Type.minus),
    ('\*', Token_Type.times),
    ('/', Token_Type.div),
    ('\(', Token_Type.open_parenthesis),
    ('\)', Token_Type.closed_parenthesis),
    ('[0-9]+', Token_Type.character),
    ('(\\ )*', Token_Type.space)],
     eof=Token_Type.eof)