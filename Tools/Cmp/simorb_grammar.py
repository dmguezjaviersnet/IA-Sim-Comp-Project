from typing import Dict
from Production import Production
from Terminal import Terminal, Eof
from Non_terminal import Non_terminal
from Grammar import Grammar
from Tools.Cmp.Own_token import Token, Token_Type
from simorb_rules import *

# Gramática del DSL

# program -> <list-statement>
# <list-statement> -> <statement> ";" <list-statement>
#                 | <statement>
# <statement> -> <let-statment>
#            | <def-func>
#            | <conditional-statement>
#            | <loop-statement>
#            | <print-statement>
# <let-statement> -> "let" ID "=" <expression>
# <def-func> -> "func" ID "(" <args-list> ")" "{" <list-statement> "}"
# <loop-statement> -> "loop" "(" <expression> ")" "{" <list-statement> "}"
# <conditional-statement> -> "if" "(" <expression> ")" "then "{" <list-statement> "}" "else" "{" <list-statement> "}"
#                          | "if" "(" <expression> ")" "then "{" <list-statement> "}"
# <print-statement> -> "print" <expression>
# <arg-list> -> ID "," <arg-list>
#             | ID
# <expression> -> <unary-expr>
#               | <binary-expr>
# <unary-expr> -> "!" <expression>
# <binary-expr> -> <term> "+" <expression>
#               | <term> "-" <expression>
#               | <term>
# <term> -> <factor> "*" <term>
#         | <factor> "/" <term>
#         | <factor> "%" <term>
#         | <factor>
# <factor> -> <atom>
#           | "(" <expression ")"
# <atom> -> NUMBER
#         | STRING
#         | BOOL
#         | ID
#         | <func-call>
# <func-call> -> ID "(" <expr-list> ")"
# <expr-list> -> <expression> "," <expr-list>
#              | <expression>

# Terminales

let_keyword = Terminal('let')
func_keyword = Terminal('func')
loop_keyword = Terminal('loop')
if_keyword = Terminal('if')
then_keyword = Terminal('then')
else_keyword = Terminal('else')
print_keyword = Terminal('print')

stmt_separator = Terminal(';')
expr_separator = Terminal(',')
assign = Terminal('=')
open_curly_braces = Terminal('{')
closed_curly_braces = Terminal('}')
open_parenthesis = Terminal('(')
closed_parenthesis = Terminal(')')
neg = Terminal('!')
addition = Terminal('+')
substraction = Terminal('-')
product = Terminal('*')
division = Terminal('/')
module = Terminal('%')

number = Terminal('Number', 'val')
boolean = Terminal('boolean', 'val')
string = Terminal('string', 'val')
var_id = Terminal('var_id', 'val')

terminals = [let_keyword, func_keyword, loop_keyword, if_keyword, then_keyword, else_keyword, print_keyword,
            stmt_separator, expr_separator, assign, open_curly_braces, closed_curly_braces, open_parenthesis,
            closed_parenthesis, neg, addition, substraction, product, division, module, number, boolean, string,
            var_id]

# No terminales

program = Non_terminal('program', 'ast')
stmt_list = Non_terminal('stmt_list', 'ast')
statement = Non_terminal('statement', 'ast')
let_stmt = Non_terminal('let_stmt', 'ast')
def_func_stmt = Non_terminal('def_func_stmt', 'ast')
conditional_stmt = Non_terminal('conditional_stmt', 'ast')
loop_stmt = Non_terminal('loop_stmt', 'ast')
print_stmt = Non_terminal('print_stmt', 'ast')
arg_list = Non_terminal('arg_list', 'ast')
expression = Non_terminal('expression', 'ast')
unary_expr = Non_terminal('unary_expr', 'ast')
binary_expr = Non_terminal('binary_expr', 'ast')
term = Non_terminal('term', 'ast')
factor = Non_terminal('factor', 'ast')
atom = Non_terminal('atom', 'ast')
func_call = Non_terminal('func_call', 'ast')
expr_list = Non_terminal('expr_list', 'ast')

non_terminals = [program, stmt_list, statement, let_stmt, def_func_stmt, conditional_stmt, loop_stmt, print_stmt,
                arg_list, expression, unary_expr, binary_expr, term, factor, atom, func_call, expr_list]

# Producciones

p1 = Production(program,
                [[stmt_list]], [[(program_rule, True)]]
                )

p2 = Production(stmt_list,
                [[statement, stmt_separator, stmt_list], [statement]],
                [[(stmt_list_rule1, True)], [(stmt_list_rule2, True)]]
                )

p3 = Production(statement,
                [[let_stmt], [def_func_stmt], [conditional_stmt], [loop_stmt], [print_stmt]]
                [[(stmt_rule1, True)], [(stmt_rule2, True)], [(stmt_rule3, True)], [(stmt_rule4, True)], [(stmt_rule5, True)]]
                )

p4 = Production(let_stmt,
                [[let_keyword, var_id, assign, expression]],
                [[(let_stmt_rule, True)]]
                )

p5 = Production (def_func_stmt,
                [[func_keyword, var_id, open_parenthesis, arg_list, closed_parenthesis, open_curly_braces, stmt_list, closed_curly_braces]],
                [[(def_func_stmt_rule, True)]]
                )

p6 = Production(loop_stmt,
                [[loop_keyword, open_parenthesis, expression, closed_parenthesis, open_curly_braces, stmt_list, closed_curly_braces]],
                [[(loop_rule, True)]]
                )

p7 = Production(conditional_stmt,
                [[if_keyword, open_parenthesis, expression, closed_parenthesis, then_keyword, stmt_list], 
                 [if_keyword, open_parenthesis, expression, closed_parenthesis, then_keyword, stmt_list, else_keyword, stmt_list]],
                [[(conditional_stmt_rule1, True)], [(conditional_stmt_rule2, True)]]
                )

p8 = Production(arg_list,
                [[var_id, expr_separator, arg_list], [var_id]],
                [[(arg_list_rule1, True)], [(arg_list_rule2, True)]]
                )

p9 = Production(expression,
                [[unary_expr], [binary_expr]],
                [[(expression_rule1, True)], [(expression_rule2, True)]]
                )

p10 = Production(unary_expr,
                [[neg, expression]],
                [[(unary_expr_rule1, True)]]
                )

p11 = Production(binary_expr,
                [[term, addition, expression], [term, substraction, expression], [term]],
                [[(binary_expr_rule1, True)], [(binary_expr_rule2, True)], [(binary_expr_rule3, True)]]
                )

p12 = Production(term,
                [[factor, product, term], [factor, product, term], [factor, module, term], [factor]],
                [[(term_rule1, True)], [(term_rule2, True)], [(term_rule3, True)], [(term_rule4, True)]]
                )

p13 = Production(factor, 
                [[atom], [open_parenthesis, expression, closed_parenthesis]],
                [[(factor_rule1, True)], [(factor_rule2, True)]]
                )

p14 = Production(atom,
                [[number], [string], [boolean], [var_id], [func_call]],
                [[(atom_rule1, True)], [(atom_rule2, True)], [(atom_rule3, True)], [(atom_rule4, True)], [(atom_rule5, True)]]
                )

p15 = Production(func_call,
                [[var_id, open_parenthesis, expr_list, closed_parenthesis]],
                [[(func_call_rule, True)]]
                )

p16 = Production(expr_list,
                [[expression, stmt_separator, expr_list], [expression]],
                [[expr_list_rule1, True], [expr_list_rule2, True]]
                )

productions = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16]

simorb_grammar = Grammar(terminals, non_terminals, productions)

token_string: Dict[Token_Type, str] = {
    Token_Type.int: 'int',
    Token_Type.float : 'float',
    Token_Type.boolean : 'boolean',
    Token_Type.string : 'string',   
    
    Token_Type.plus : '+',
    Token_Type.minus : '-',
    Token_Type.times : '*',
    Token_Type.div : '/',
    Token_Type.mod : '%',
    Token_Type.neg : '!',

    Token_Type.loop : 'loop',
    Token_Type.func : 'func',
    Token_Type.if_simorb : 'if',
    Token_Type.then : 'then',
    Token_Type.else_simorb : 'else',
    Token_Type.let : 'let',

    Token_Type.assign : '=',
    Token_Type.open_parenthesis : '(',
    Token_Type.closed_parenthesis : ')',
    Token_Type.open_curly_braces : '{',
    Token_Type.closed_curly_braces : '}',

    Token_Type.eof : '$',
    Token_Type.space : ' '
}
