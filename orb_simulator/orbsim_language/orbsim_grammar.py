from typing import Dict
from parser.production import Production
from parser.terminal import Terminal, Eof, Epsilon
from parser.non_terminal import Non_terminal
from parser.grammar import Grammar
from parser.own_token import Token, Token_Type
from orbsim_language.orbsim_rules import *

# Gramática del DSL
'''
program -> <list-statement>
<list-statement> -> <statement> ";" <list-statement>
                | <statement> ";"
<statement> -> <let-statment>
           | <def-func>
           | <conditional-statement>
           | <loop-statement>
           | <print-statement>
<let-statement> -> "let" ID "=" <expression> ;
<def-func> -> "func" ID "(" <args-list> ")" "{" <list-statement> "}"
<loop-statement> -> "loop" "(" <expression> ")" "{" <list-statement> "}"
<conditional-statement> -> "if" "(" <expression> ")" "then "{" <list-statement> "}" "else" "{" <list-statement> "}"
                         | "if" "(" <expression> ")" "then "{" <list-statement> "}"
<print-statement> -> "print" <expression>
<arg-list> -> ID "," <arg-list>
            | ID
<expression> -> or_expr
              |
<or-expr> -> <and-expr> "||" <or-expr>
           | <and-expr>
<and-expr> -> <not-expr> "&&" <and-expr>
            | <not-expr>
<not-expr> -> ! <not-expr>
            | <compare-expr>
<compare-expr> -> <arth-expr> <compare-op> <compare-expr>
               | <arth-expr>
<compare-op> ->  ">"
               | "<"
               | ">="
               | "<="
               | "=="
               | "!="
# <bitwise-or> -> <bitwise-xor> "|" <bitwise-or>
#                 | <bitwise-xor>
# <bitwise-xor> -> <bitwise-and> "^" <bitwise-xor>
#               | <bitwise-and>
# <bitwise-and> -> <shift> "&" <bitwise-and>
#                | <shift>
# <shift> -> <arth-exp> "<<" <shift>
#         | <arth-exp> ">>" <shift>
#         | <arth-expr>
<arth-expr> -> <arth-expr> + <term>
             | <arth-expr> - <term>
             | <term>
<term> -> <term> "*" <factor> 
        | <term> "/" <factor>
        | <term> "%" <factor> 
        | <factor>
<factor> -> <atom>
          | "(" <expression> ")"
<atom> -> INT
        | FLOAT 
        | STRING
        | BOOL
        | ID
        | <func-call>
<func-call> -> ID "(" <expr-list> ")"
<expr-list> -> <expression> "," <expr-list>
             | <expression>
'''
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
logic_or = Terminal('||')
logic_and = Terminal('&&')
not_equals = Terminal('!=')
equals = Terminal('==')
greater_or_equal = Terminal('>=')
less_equal = Terminal('<=')
greater = Terminal('>')
less = Terminal('<')
addition = Terminal('+')
substraction = Terminal('-')
product = Terminal('*')
division = Terminal('/')
module = Terminal('%')
eof = Eof()

int = Terminal('int', 'val')
float = Terminal('float', 'val')
boolean = Terminal('boolean', 'val')
string = Terminal('string', 'val')
id_orbsim = Terminal('id_orbsim', 'val')

terminals = [let_keyword, func_keyword, loop_keyword, if_keyword, then_keyword, else_keyword, print_keyword,
            stmt_separator, expr_separator, assign, open_curly_braces, closed_curly_braces, open_parenthesis,
            closed_parenthesis, neg, logic_or, logic_and, not_equals, equals, greater_or_equal, less_equal,
            greater, less, addition, substraction, product, division, module, int, float, boolean, 
            string, id_orbsim, eof]

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
or_expr = Non_terminal('or_expr', 'ast')
and_expr = Non_terminal('and_expr', 'ast')
not_expr = Non_terminal('not_expr', 'ast')
compare_expr = Non_terminal('compare_expr', 'ast')
compare_op = Non_terminal('compare_op', 'ast')
arth_expr = Non_terminal('arth_expr', 'ast')
term = Non_terminal('term', 'ast')
factor = Non_terminal('factor', 'ast')
atom = Non_terminal('atom', 'ast')
func_call = Non_terminal('func_call', 'ast')
expr_list = Non_terminal('expr_list', 'ast')

non_terminals = [program, stmt_list, statement, let_stmt, def_func_stmt, conditional_stmt, loop_stmt, print_stmt,
                arg_list, expression,or_expr, and_expr, not_expr, compare_expr, compare_op, arth_expr, term, factor,
                atom, func_call, expr_list]

# Producciones

p1 = Production(program,
                [[stmt_list]], [[(program_rule, True)]]
                )

p2 = Production(stmt_list,
                [[statement, stmt_separator, stmt_list], [statement, stmt_separator]],
                [[(stmt_list_rule1, True)], [(stmt_list_rule2, True)]]
                )

p3 = Production(statement,
                [[let_stmt], [def_func_stmt], [conditional_stmt], [loop_stmt], [print_stmt]],
                [[(stmt_rule1, True)], [(stmt_rule2, True)], [(stmt_rule3, True)], [(stmt_rule4, True)], [(stmt_rule5, True)]]
                )

p4 = Production(let_stmt,
                [[let_keyword, id_orbsim, assign, expression]],
                [[(let_stmt_rule, True)]]
                )

p5 = Production (def_func_stmt,
                [[func_keyword, id_orbsim, open_parenthesis, arg_list, closed_parenthesis, open_curly_braces, stmt_list, closed_curly_braces]],
                [[(def_func_stmt_rule, True)]]
                )

p6 = Production(loop_stmt,
                [[loop_keyword, open_parenthesis, expression, closed_parenthesis, open_curly_braces, stmt_list, closed_curly_braces]],
                [[(loop_rule, True)]]
                )

p7 = Production(conditional_stmt,
                [[if_keyword, open_parenthesis, expression, closed_parenthesis, then_keyword, open_curly_braces,
                 stmt_list, closed_curly_braces], 
                 [if_keyword, open_parenthesis, expression, closed_parenthesis, then_keyword, open_curly_braces,
                 stmt_list, closed_curly_braces, else_keyword, stmt_list]],
                [[(conditional_stmt_rule1, True)], [(conditional_stmt_rule2, True)]]
                )

p8 = Production(arg_list,
                [[id_orbsim, expr_separator, arg_list], [id_orbsim]],
                [[(arg_list_rule1, True)], [(arg_list_rule2, True)]]
                )

p9 = Production(expression,
                [[or_expr]],
                [[(expression_rule1, True)]]
                )

p10 = Production(or_expr,
                [[and_expr, logic_or, or_expr], [and_expr]],
                [[(or_expr_rule1, True)], [(or_expr_rule2, True)]]
                )

p11 = Production(and_expr,
                [[not_expr, logic_and, and_expr], [not_expr]],
                [[(and_expr_rule1, True)], [(and_expr_rule2, True)]]
                )

p12 = Production(not_expr,
                [[neg, not_expr], [compare_expr]],
                [[(not_expr_rule1, True)], [(not_expr_rule2, True)]]
                )

p13 = Production(compare_expr, 
                [[arth_expr, compare_op, compare_expr], [arth_expr]],
                [[(compare_expr_rule1, True)], [(compare_expr_rule2, True)]]
                )

p14 = Production(compare_op,
                [[equals], [not_equals], [greater_or_equal], [less_equal], [greater], [less]],
                [[(compare_op_rule, True)], [(compare_op_rule, True)], [(compare_op_rule, True)], 
                 [(compare_op_rule, True)], [(compare_op_rule, True)], [(compare_op_rule, True)]]
                )

p15 = Production(arth_expr,
                [[arth_expr, addition, term], [arth_expr, substraction, term], [term]],
                [[(arth_expr_rule1, True)], [(arth_expr_rule2, True)], [(arth_expr_rule3, True)]]
                )

p16 = Production(term,
                [[term, product, factor], [term, division, factor], [term, module, factor], [factor]],
                [[(term_rule1, True)], [(term_rule2, True)], [(term_rule3, True)], [(term_rule4, True)]]
                )

p17 = Production(factor,
                [[atom], [open_parenthesis, expression, closed_parenthesis]],
                [[(factor_rule1, True)], [(factor_rule2, True)]]
                )

p18 = Production(atom,
                [[int], [float], [boolean], [string], [id_orbsim], [func_call]],
                [[(atom_rule1, True)], [(atom_rule2, True)], [(atom_rule3, True)], 
                 [(atom_rule4, True)], [(atom_rule5, True)], [(atom_rule6, True)]]
                )

p19 = Production(func_call,
                [[id_orbsim, open_parenthesis, expr_list, closed_parenthesis]],
                [[(func_call_rule, True)]]
                )

p20 = Production(expr_list,
                [[expression, stmt_separator, expr_list], [expression]],
                [[expr_list_rule1, True], [expr_list_rule2, True]]
                )

productions = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20]

orbsim_grammar = Grammar(terminals, non_terminals, program, productions)

orbsim_token_string: Dict[Token_Type, str] = {
    Token_Type.loop : 'loop',
    Token_Type.func : 'func',
    Token_Type.if_orbsim : 'if',
    Token_Type.then : 'then',
    Token_Type.else_orbsim : 'else',
    Token_Type.let : 'let',
    
    Token_Type.int: 'int',
    Token_Type.float : 'float',
    Token_Type.boolean : 'boolean',
    Token_Type.string : 'string',
    Token_Type.id_orbsim : 'id_orbsim',
    
    Token_Type.plus : '+',
    Token_Type.minus : '-',
    Token_Type.mul : '*',
    Token_Type.div : '/',
    Token_Type.mod : '%',
    Token_Type.neg : '!',

    Token_Type.equals: '==',
    Token_Type.not_equals: '!=',
    Token_Type.greater_or_equal_than: '>=',
    Token_Type.less_or_equal_than: '<=',
    Token_Type.greater_than: '>',
    Token_Type.less_than: '<',

    Token_Type.assign : '=',
    Token_Type.open_parenthesis : '(',
    Token_Type.closed_parenthesis : ')',
    Token_Type.open_curly_braces : '{',
    Token_Type.closed_curly_braces : '}',

    Token_Type.stmt_separator : ';',
    Token_Type.expr_separator : ',',

    Token_Type.eof : '$',
    Token_Type.space : ' ',
    Token_Type.new_line : '\n'
}
