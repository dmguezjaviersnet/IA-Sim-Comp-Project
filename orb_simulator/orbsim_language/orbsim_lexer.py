from lexer import Lexer
from parser.own_token import Token_Type

orbsim_lexer = Lexer([
    ('loop', Token_Type.loop),
    ('func', Token_Type.func),
    ('if', Token_Type.if_orbsim),
    ('then', Token_Type.then),
    ('else', Token_Type.else_orbsim),
    ('let', Token_Type.let),
    ('ret', Token_Type.return_orbsim),
    ('([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*', Token_Type.id_orbsim),
    ('0|([1-9][0-9]*)', Token_Type.int),
    ('(0|([1-9][0-9]*)).[0-9]+', Token_Type.float),
    ('true|false', Token_Type.boolean),
    ('\'    \'', Token_Type.string),
    ('\+', Token_Type.plus),
    ('\-', Token_Type.minus),
    ('\*', Token_Type.mul),
    ('/', Token_Type.div),
    ('%', Token_Type.mod),
    ('=', Token_Type.assign),
    ('==', Token_Type.equals),
    ('!=', Token_Type.not_equals),
    ('!', Token_Type.neg),
    ('<', Token_Type.less_than),
    ('>', Token_Type.greater_than),
    ('<=', Token_Type.less_or_equal_than),
    ('>=', Token_Type.greater_or_equal_than),
    ('\|\|', Token_Type.logical_or),
    ('&&', Token_Type.logical_and),
    ('\(', Token_Type.open_parenthesis),
    ('\)', Token_Type.closed_parenthesis),
    ('{', Token_Type.open_curly_braces),
    ('}', Token_Type.closed_curly_braces),
    (';', Token_Type.stmt_separator),
    (',', Token_Type.expr_separator),
    ('(\\ )+', Token_Type.space),
    ('(\\n)+', Token_Type.new_line),
    ('([a-z]|[A-Z]|[0-9]|\\! | \\@| \\# | \\$| \\%| \\^| \\&| \\*| \\( | \\) | \\~ | \\/  | \\- | \\+ )*', Token_Type.error)],
    eof=Token_Type.eof)