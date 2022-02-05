from lr1_parser import lr1_parse
from lexer import Lexer
from arth_grammar import arth_grammar, arth_grammar_token_string
from own_token import Token_Type

def test_parse():

    ##### Probando LR(1) con gramática aritmética #####

    lex = Lexer([('\+', Token_Type.plus),
    ('\-', Token_Type.minus),
    ('\*', Token_Type.times),
    ('/', Token_Type.div),
    ('\(', Token_Type.open_parenthesis),
    ('\)', Token_Type.closed_parenthesis),
    ('[0-9]+', Token_Type.character),
    ('(\\ )*', Token_Type.space)],
     eof=Token_Type.eof)

    tokens1 = lex('(3 + 5)*(4/(5 - 8))')
    tokens2 = lex('(3 + 5)*')
    tokens3 = lex('(3 + 5)*(')
    tokens4 = lex('(3 + 5)*(4)')
    tokens5 = lex('(())')
    tokens6 = lex('(3 + 5)*4')
    tokens7 = lex('(3 ++ 5)*(4/(5 - 8))')
    tokens8 = lex('(3 + 5)**(4/(5 - 8))')
    tokens9 = lex('(3 + 5)*(44/(5 - 800))')
    tokens10 = lex('3*(* 4 - 5)')

    success1, ast = lr1_parse(arth_grammar, tokens1, arth_grammar_token_string)
    success2, ast = lr1_parse(arth_grammar, tokens2, arth_grammar_token_string)
    success3, ast = lr1_parse(arth_grammar, tokens3, arth_grammar_token_string)
    success4, ast = lr1_parse(arth_grammar, tokens4, arth_grammar_token_string)
    success5, ast = lr1_parse(arth_grammar, tokens5, arth_grammar_token_string)
    success6, ast = lr1_parse(arth_grammar, tokens6, arth_grammar_token_string)
    success7, ast = lr1_parse(arth_grammar, tokens7, arth_grammar_token_string)
    success8, ast = lr1_parse(arth_grammar, tokens8, arth_grammar_token_string)
    success9, ast = lr1_parse(arth_grammar, tokens9, arth_grammar_token_string)
    success10, ast = lr1_parse(arth_grammar, tokens10, arth_grammar_token_string)

    assert success1 == True
    assert success2 == False
    assert success3 == False
    assert success4 == True
    assert success5 == False
    assert success6 == True
    assert success7 == False
    assert success8 == False
    assert success9 == True
    assert success10 == False
