from Lexer import Lexer
from Own_token import Token_Type

simorb_lexer = Lexer([
    ('loop', Token_Type.loop),
    ('if', Token_Type.if_simorb),
    ('then', Token_Type.then),
    ('else', Token_Type.else_simorb),
    ('let', Token_Type.let),
    ('[a-z]|[A-Z]|([a-z]|[A-Z]|[0-9])*', Token_Type.id_orbsim),
    ('[1-9][0-9]*', Token_Type.int),
    ('(0|([1-9][0-9]*)).[0-9]+', Token_Type.float),
    ('true|false', Token_Type.boolean),
    ('\'    \'', Token_Type.string),
    ('\+', Token_Type.plus),
    ('\-', Token_Type.minus),
    ('\*', Token_Type.times),
    ('/', Token_Type.div),
    ('%', Token_Type.mod),
    ('\(', Token_Type.open_parenthesis),
    ('\)', Token_Type.closed_parenthesis),
    ('{', Token_Type.open_curly_braces),
    ('}', Token_Type.closed_curly_braces),
    ('(\\ )*', Token_Type.space)],
    eof=Token_Type.eof)