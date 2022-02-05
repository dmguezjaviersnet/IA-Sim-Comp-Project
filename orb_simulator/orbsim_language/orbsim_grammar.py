from typing import Dict
from parser.production import Production
from parser.terminal import Terminal, Eof
from parser.non_terminal import Non_terminal
from parser.grammar import Grammar
from parser.own_token import Token_Type
from orbsim_language.orbsim_rules import class_body_stmt_list_rule1, class_body_stmt_list_rule1, class_body_stmt_list_rule2
from orbsim_language.orbsim_rules import class_body_stmt_rule, attr_stmt_rule, def_func_stmt_rule, func_body_stmt_list_rule1
from orbsim_language.orbsim_rules import func_body_stmt_list_rule2 
from orbsim_language.orbsim_rules import and_expr_rule1, and_expr_rule2, arg_list_rule1, arg_list_rule2, arth_expr_rule1
from orbsim_language.orbsim_rules import arth_expr_rule2, arth_expr_rule3, atom_rule1, atom_rule2, atom_rule3, atom_rule4
from orbsim_language.orbsim_rules import atom_rule5, atom_rule6, bitwise_and_expr_rule1, bitwise_and_expr_rule2
from orbsim_language.orbsim_rules import bitwise_or_expr_rule1, bitwise_or_expr_rule2, bitwise_shift_expr_rule1
from orbsim_language.orbsim_rules import bitwise_shift_expr_rule2, bitwise_shift_expr_rule3, bitwise_xor_expr_rule1
from orbsim_language.orbsim_rules import bitwise_xor_expr_rule2, compare_expr_rule1, compare_expr_rule2, compare_op_rule
from orbsim_language.orbsim_rules import conditional_body_stmt_list_rule1, conditional_body_stmt_list_rule2
from orbsim_language.orbsim_rules import conditional_body_stmt_rule, conditional_stmt_rule1, conditional_stmt_rule2
from orbsim_language.orbsim_rules import expr_list_rule1, expr_list_rule2, expression_rule1, factor_rule1, factor_rule2
from orbsim_language.orbsim_rules import func_body_stmt_rule, func_call_rule, let_stmt_rule, loop_body_stmt_list_rule1
from orbsim_language.orbsim_rules import loop_body_stmt_list_rule2, loop_body_stmt_rule, loop_stmt_rule, not_expr_rule1
from orbsim_language.orbsim_rules import not_expr_rule2, or_expr_rule1, or_expr_rule2, program_rule, ret_stmt_rule
from orbsim_language.orbsim_rules import stmt_list_rule1, stmt_list_rule2, stmt_rule1, stmt_rule2, term_rule1, term_rule2
from orbsim_language.orbsim_rules import term_rule3, term_rule4

# Gramática del DSL
'''
############### Grammar 1 ###################
program -> statement_list ########## Prod 1
statement_list -> statement ; statement_list  ########## Prod 2
            | statement
statement -> class { class_body_stmt_list } ; ########## Prod 3
           | let_stmt
           | assign_stmt
           | loop_stmt
           | conditional_stmt
           | print_stmt
           | def_func_stmt
class_body_stmt_list -> class_body_stmt ; class_body_stmt_list ########## Prod 4
               | class_body_stmt ;
class_body_stmt -> def_func_stmt ########## Prod 5
                | attr_stmt
attr_stmt -> type ID ; ########## Prod 6
def_func_stmt -> func type ID ( args_list_expr ) { func_body_stmt_list } ; ########## Prod 7
func_body_stmt_list -> func_body_stmt ; func_body_stmt_list ########## Prod 8
                | func_body_stmt ;         
func_body_stmt -> let_stmt ########## Prod 9
             | assign_stmt
             | loop_stmt
             | conditional_stmt
             | ret_stmt
let_stmt -> let type ID = expression ########## Prod 10
assign_stmt ->  ID = expression ########## Prod 11
loop_stmt -> loop ( condition ) { loop_body_list_stmt } ; ########## Prod 12
loop_body_list_stmt -> loop_body_stmt ; loop_body_list_stmt ########## Prod 13
                    | loop_body_stmt ;
loop_body_stmt -> let_stmt ########## Prod 14
             | assign_stmt
             | loop_stmt
             | conditional_stmt
             | flow_stmt
flow_stmt -> break ########## Prod 15
           | continue
conditional_stmt -> if ( condition ) then { conditional_body_stmt_list } ; ########## Prod 16
              | if ( condition ) then { conditional_body_stmt_list } else { conditional_body_stmt_list } ;
conditional_body_stmt_list -> conditional_body_stmt ; conditional_body_stmt_list  ########## Prod 17
                                | conditional_body_stmt ;
conditional_body_stmt -> let_stmt ########## Prod 18
             | assign_stmt
             | loop_stmt
             | conditional_stmt
ret_stmt -> ret expression ########## Prod 19
print_statement -> print expression ########## Prod 20
arg_list -> ID , arg_list ########## Prod 21
            | ID
expression -> or_expr ########## Prod 22
              |
or_expr -> and_expr "||" or_expr ########## Prod 23
          | and_expr
and_expr -> not_expr "&&" and_expr  ########## Prod 24
            | not_expr
not_expr -> ! not_expr ########## Prod 25
           | compare_expr
compare_expr -> bitwise_or_expr compare-op compare_expr ########## Prod 26
              | bitwise_or_expr
compare-op ->  ">" ########## Prod 27
                | "<"
                | ">="
                | "<="
                | "=="
                | "!="
bitwise_or_expr -> bitwise_xor_expr "|" bitwise_or_expr ########## Prod 28
               | bitwise_xor_expr
bitwise_xor_expr -> bitwise_and_expr "^" bitwise_xor_expr ########## Prod 29
                | bitwise_and_expr
bitwise_and_expr -> shift_expr "&" bitwise_and_expr ########## Prod 30
                | shift_expr
shift_expr -> arth_exp << shift_expr ########## Prod 31
        | arth_exp >> shift_expr
        | arth_expr
arth_expr -> term + arth_expr ########## Prod 32
            | term - arth_expr
            | term
term -> factor "*" term ########## Prod 33
       | factor "/" term
       | factor "%" term
       | factor
factor -> atom ########## Prod 34
         | ( expression )
atom -> INT ########## Prod 35
       | FLOAT 
       | STRING
       | BOOL
       | ID
       | func_call
       | method_call
       | make_instance
func_call -> ID ( expr_list ) ########## Prod 36
make_instance -> make ID ( expr_list ) ########## Prod 37
method_call -> ID . ID ( expr_list ) ########## Prod 38
expr_list -> expression "," expr_list ########## Prod 39
             | expression>


############### Grammar 2 ###################
program -> list_statement
list_statement -> statement ";" list_statement
               | statement ";"
statement> -> let_statement
           | def_func
           | conditional_statement
           | loop_statement
           | print-statement
           | ret-statement
ret-statement -> "ret" expression
let_statement -> "let" ID "=" expression
def_func -> "func" ID "(" args-list ")" "{" list_statement "}"
loop_statement -> "loop" "(" expression ")" "{" list_statement "}"
conditional_statement -> "if" "(" expression ")" "then "{" list_statement "}" "else" "{" list_statement "}"
                         | "if" "(" expression ")" "then "{" list_statement "}"
print-statement -> "print" expression
arg-list -> ID "," arg-list
           | ID
expression -> or_expr
              |
or_expr -> <and_expr> "||" <or_expr>
          | <and_expr>
and_expr -> not_expr "&&" and_expr
           | not_expr
not_expr -> ! not_expr
           | compare_expr
compare_expr -> bitwise_or compare-op compare_expr
              | bitwise_or
compare_op ->  ">"
               | "<"
               | ">="
               | "<="
               | "=="
               | "!="
 bitwise_or -> bitwise_xor "|" bitwise_or
                | bitwise_xor
 bitwise_xor -> bitwise_and "^" bitwise_or
              | bitwise_and
 bitwise_and -> shift "&" bitwise_and
               | shift
 shift -> arth-exp "<<" shift
         | arth-exp ">>" shift
         | arth-expr
arth_expr -> arth_expr + term
             | arth_expr - term
             | term
term -> term "*" factor
        | term "/" factor
        | term "%" factor
        | factor
factor -> atom
          | "(" <expression> ")"
atom -> INT
        | FLOAT 
        | STRING
        | BOOL
        | ID
        | func_call
func_call -> ID "(" <expr-list> ")"
expr_list -> expression "," expr_list
             | expression
'''
# Terminales

let_keyword = Terminal('let')
func_keyword = Terminal('func')
loop_keyword = Terminal('loop')
class_keyword = Terminal('class')
if_keyword = Terminal('if')
then_keyword = Terminal('then')
else_keyword = Terminal('else')
print_keyword = Terminal('print')
break_keyword = Terminal('break')
continue_keyword = Terminal('continue')
ret_keyword = Terminal('ret')
make_keyword = Terminal('make')

stmt_separator = Terminal(';')
expr_separator = Terminal(',')
class_member_access_operator = Terminal('.')
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
bitwise_or = Terminal('|')
bitwise_xor = Terminal('^')
bitwise_and = Terminal('&')
bitwise_shift_left = Terminal('<<')
bitwise_shift_right = Terminal('>>')
addition = Terminal('+')
substraction = Terminal('-')
product = Terminal('*')
division = Terminal('/')
module = Terminal('%')
eof = Eof()

int = Terminal('int_val', 'val')
float = Terminal('float_val', 'val')
boolean = Terminal('boolean_val', 'val')
string = Terminal('string_val', 'val')
id_orbsim = Terminal('id_orbsim', 'val')
type_id = Terminal('type_id', 'val')

terminals = [class_keyword, let_keyword, func_keyword, loop_keyword, if_keyword, then_keyword, else_keyword, print_keyword,
            break_keyword, continue_keyword, ret_keyword, make_keyword, stmt_separator, expr_separator, assign,
            open_curly_braces, closed_curly_braces, open_parenthesis, closed_parenthesis, neg, logic_or, logic_and,
            not_equals, equals, greater_or_equal, less_equal, greater, less, addition, substraction, product, division,
            module, int, float, boolean, string, id_orbsim, eof, type_id, bitwise_or, bitwise_xor, bitwise_and,
            bitwise_shift_left, bitwise_shift_right]

# No terminales

program = Non_terminal('program', 'ast')
stmt_list = Non_terminal('stmt_list', 'ast')
statement = Non_terminal('statement', 'ast')
class_body_stmt_list = Non_terminal('class_body_stmt_list', 'ast')
class_body_stmt = Non_terminal('class_body_stmt', 'ast')
attr_stmt = Non_terminal('attr_stmt', 'ast')
def_func_stmt = Non_terminal('def_func_stmt', 'ast')
func_body_stmt_list = Non_terminal('func_body_stmt_list', 'ast')
func_body_stmt = Non_terminal('func_body_stmt', 'ast')
let_stmt = Non_terminal('let_stmt', 'ast')
assign_stmt = Non_terminal('assign_stmt', 'ast')
loop_stmt = Non_terminal('loop_stmt', 'ast')
conditional_stmt = Non_terminal('conditional_stmt', 'ast')
print_stmt = Non_terminal('print_stmt', 'ast')
ret_stmt = Non_terminal('ret_stmt', 'ast')
loop_body_stmt_list = Non_terminal('loop_body_stmt_list', 'ast')
loop_body_stmt = Non_terminal('loop_body_stmt', 'ast')
flow_stmt = Non_terminal('flow_stmt', 'ast')
conditional_body_stmt_list = Non_terminal('conditional_body_stmt_list', 'ast')
conditional_body_stmt = Non_terminal('conditional_body_stmt', 'ast')
arg_list = Non_terminal('arg_list', 'ast')

expression = Non_terminal('expression', 'ast')
or_expr = Non_terminal('or_expr', 'ast')
and_expr = Non_terminal('and_expr', 'ast')
not_expr = Non_terminal('not_expr', 'ast')
compare_expr = Non_terminal('compare_expr', 'ast')
compare_op = Non_terminal('compare_op', 'ast')
bitwise_or_expr = Non_terminal('bitwise_or_expr', 'ast')
bitwise_xor_expr = Non_terminal('bitwise_xor_expr', 'ast')
bitwise_and_expr = Non_terminal('bitwise_and_expr', 'ast')
shift_expr = Non_terminal('shift_expr', 'ast')
arth_expr = Non_terminal('arth_expr', 'ast')
term = Non_terminal('term', 'ast')
factor = Non_terminal('factor', 'ast')
atom = Non_terminal('atom', 'ast')
func_call = Non_terminal('func_call', 'ast')
make_instance = Non_terminal('make_instance', 'ast')
method_call = Non_terminal('method_call', 'ast')
expr_list = Non_terminal('expr_list', 'ast')

non_terminals = [program, stmt_list, statement, class_body_stmt_list, class_body_stmt, attr_stmt, def_func_stmt, 
                func_body_stmt_list, func_body_stmt, let_stmt, assign_stmt, loop_stmt, conditional_stmt, print_stmt,
                ret_stmt, loop_body_stmt_list, loop_body_stmt, flow_stmt, conditional_body_stmt_list, conditional_body_stmt,
                arg_list, expression, or_expr, and_expr, not_expr, compare_expr, compare_op, bitwise_or_expr, bitwise_xor_expr,
                bitwise_and_expr, shift_expr, arth_expr, term, factor, atom, func_call, make_instance, method_call, expr_list]

# Producciones

p1 = Production(program,
                [[stmt_list]], [[(program_rule, True)]]
                )

p2 = Production(stmt_list,
                [[statement, stmt_separator, stmt_list], [statement, stmt_separator]],
                [[(stmt_list_rule1, True)], [(stmt_list_rule2, True)]]
                )

p3 = Production(statement,
                [[class_keyword, type_id, open_curly_braces, class_body_stmt_list, closed_curly_braces], 
                 [let_stmt], 
                 [def_func_stmt], 
                 [conditional_stmt], 
                 [loop_stmt], 
                 [print_stmt],
                 [assign_stmt]], 
                [[(stmt_rule1, True)], [(stmt_rule2, True)], [(stmt_rule2, True)], 
                 [(stmt_rule2, True)], [(stmt_rule2, True)], [(stmt_rule2, True)], [(stmt_rule2, True)]]
                )

p4 = Production(class_body_stmt_list,
                [[class_body_stmt, stmt_separator, class_body_stmt_list],
                 [class_body_stmt, stmt_separator]],
                 [[(class_body_stmt_list_rule1, True)], [(class_body_stmt_list_rule2, True)]]
                )

p5 = Production(class_body_stmt,
                [[attr_stmt], 
                 [def_func_stmt]], 
                [[(class_body_stmt_rule, True)], [(class_body_stmt_rule, True)]]
                )

p6 = Production(attr_stmt,
                [[type_id, id_orbsim]],
                [[(attr_stmt_rule, True)]]
                )

p7 = Production (def_func_stmt,
                [[func_keyword, type_id, id_orbsim, open_parenthesis, arg_list, closed_parenthesis,
                 open_curly_braces, func_body_stmt_list, closed_curly_braces]],
                [[(def_func_stmt_rule, True)]]
                )

p8 = Production (func_body_stmt_list,
                [[func_body_stmt, stmt_separator, func_body_stmt_list], [func_body_stmt, stmt_separator]],
                [[(func_body_stmt_list_rule1, True)], [(func_body_stmt_list_rule2, True)]]
                )

p9 = Production (func_body_stmt,
                [[let_stmt], [assign_stmt], [loop_stmt], [conditional_stmt], [ret_stmt]],
                [[(func_body_stmt_rule, True)], [(func_body_stmt_rule, True)], [(func_body_stmt_rule, True)],
                 [(func_body_stmt_rule, True)], [(func_body_stmt_rule, True)]]
                )

p10 = Production(let_stmt,
                [[let_keyword, type_id, id_orbsim, assign, expression]],
                [[(let_stmt_rule, True)]]
                )

p11 = Production(assign_stmt,
                [[id_orbsim, assign, expression]],
                [[(let_stmt_rule, True)]]
                )

p12 = Production(loop_stmt,
                [[loop_keyword, open_parenthesis, expression, closed_parenthesis, open_curly_braces, loop_body_stmt_list,
                 closed_curly_braces, stmt_separator]],
                [[(loop_stmt_rule, True)]]
                )

p13 = Production(loop_body_stmt_list,
                [[loop_body_stmt, stmt_separator, loop_body_stmt_list], [loop_body_stmt, stmt_separator]],
                [[(loop_body_stmt_list_rule1, True)], [(loop_body_stmt_list_rule2, True)]]
                )

p14 = Production(loop_body_stmt,
                [[let_stmt], [assign_stmt], [loop_stmt], [conditional_stmt], [flow_stmt]],
                [[(loop_body_stmt_rule, True)], [(loop_body_stmt_rule, True)], [(loop_body_stmt_rule, True)],
                 [(loop_body_stmt_rule, True)], [(loop_body_stmt_rule, True)]]
                )

p15 = Production(flow_stmt,
                [[continue_keyword], [break_keyword]],
                [[(atom_rule1, True)], [(atom_rule1, True)]]
                )

p16 = Production(conditional_stmt,
                [[if_keyword, open_parenthesis, expression, closed_parenthesis, then_keyword, open_curly_braces,
                 conditional_body_stmt_list, closed_curly_braces], 
                 [if_keyword, open_parenthesis, expression, closed_parenthesis, then_keyword, open_curly_braces,
                 conditional_body_stmt_list, closed_curly_braces, else_keyword, open_curly_braces, conditional_body_stmt_list,
                 closed_curly_braces]],
                [[(conditional_stmt_rule1, True)], [(conditional_stmt_rule2, True)]]
                )

p17 = Production(conditional_body_stmt_list,
                [[conditional_body_stmt, stmt_separator, conditional_body_stmt_list], [conditional_body_stmt, stmt_separator]],
                [[(conditional_body_stmt_list_rule1, True)], [(conditional_body_stmt_list_rule2, True)]]
                )

p18 = Production(conditional_body_stmt,
                [[let_stmt], [assign_stmt], [loop_stmt], [conditional_stmt], [ret_stmt]],
                [[(conditional_body_stmt_rule, True)], [(conditional_body_stmt_rule, True)],
                 [(conditional_body_stmt_rule, True)], [(conditional_body_stmt_rule, True)], [(conditional_body_stmt_rule, True)]]
                )

p19 = Production(ret_stmt,
                [[ret_keyword, expression]],
                [[(ret_stmt_rule, True)]]
                )

p20 = Production(print_stmt,
                [[print_keyword, expression]],
                [[(atom_rule1, True)]]
                )

p21 = Production(arg_list,
                [[id_orbsim, expr_separator, arg_list], [id_orbsim]],
                [[(arg_list_rule1, True)], [(arg_list_rule2, True)]]
                )

p22 = Production(expression,
                [[or_expr]],
                [[(expression_rule1, True)]]
                )

p23 = Production(or_expr,
                [[and_expr, logic_or, or_expr], [and_expr]],
                [[(or_expr_rule1, True)], [(or_expr_rule2, True)]]
                )

p24 = Production(and_expr,
                [[not_expr, logic_and, and_expr], [not_expr]],
                [[(and_expr_rule1, True)], [(and_expr_rule2, True)]]
                )

p25 = Production(not_expr,
                [[neg, not_expr], [compare_expr]],
                [[(not_expr_rule1, True)], [(not_expr_rule2, True)]]
                )

p26 = Production(compare_expr, 
                [[bitwise_or_expr, compare_op, compare_expr], [bitwise_or_expr]],
                [[(compare_expr_rule1, True)], [(compare_expr_rule2, True)]]
                )

p27 = Production(compare_op,
                [[equals], [not_equals], [greater_or_equal], [less_equal], [greater], [less]],
                [[(compare_op_rule, True)], [(compare_op_rule, True)], [(compare_op_rule, True)], 
                 [(compare_op_rule, True)], [(compare_op_rule, True)], [(compare_op_rule, True)]]
                )

p28 = Production(bitwise_or_expr,
                [[bitwise_xor_expr, bitwise_or, bitwise_or_expr], [bitwise_xor_expr]],
                [[(bitwise_or_expr_rule1, True)], [(bitwise_or_expr_rule2, True)]]
                )

p29 = Production(bitwise_xor_expr,
                [[bitwise_and_expr, bitwise_xor, bitwise_xor_expr], [bitwise_and_expr]],
                [[(bitwise_xor_expr_rule1, True)], [(bitwise_xor_expr_rule2, True)]]
                )

p30 = Production(bitwise_and_expr,
                [[shift_expr, bitwise_and, bitwise_and_expr], [shift_expr]],
                [[(bitwise_and_expr_rule1, True)], [(bitwise_and_expr_rule2, True)]]
                )

p31 = Production(shift_expr,
                [[arth_expr, bitwise_shift_left, shift_expr], [arth_expr, bitwise_shift_right, shift_expr], [arth_expr]],
                [[(bitwise_shift_expr_rule1, True)], [(bitwise_shift_expr_rule2, True)], [(bitwise_shift_expr_rule3, True)]]
                )

p32 = Production(arth_expr,
                [[term, addition, arth_expr], [term, substraction, arth_expr], [term]],
                [[(arth_expr_rule1, True)], [(arth_expr_rule2, True)], [(arth_expr_rule3, True)]]
                )

p33 = Production(term,
                [[factor, product, term], [factor, division, term], [factor, module, term], [factor]],
                [[(term_rule1, True)], [(term_rule2, True)], [(term_rule3, True)], [(term_rule4, True)]]
                )

p34 = Production(factor,
                [[atom], [open_parenthesis, expression, closed_parenthesis]],
                [[(factor_rule1, True)], [(factor_rule2, True)]]
                )

p35 = Production(atom,
                [[int], [float], [boolean], [string], [id_orbsim], [func_call]],
                [[(atom_rule1, True)], [(atom_rule2, True)], [(atom_rule3, True)], 
                 [(atom_rule4, True)], [(atom_rule5, True)], [(atom_rule6, True)]]
                )

p36 = Production(func_call,
                [[id_orbsim, open_parenthesis, expr_list, closed_parenthesis]],
                [[(func_call_rule, True)]]
                )

p37 = Production(method_call,
                [[id_orbsim, class_member_access_operator, open_parenthesis, expr_list, closed_parenthesis]],
                [[(func_call_rule, True)]]
                )

p38 = Production(make_instance,
                [[make_keyword, type_id, open_parenthesis, expr_list, closed_parenthesis]],
                [[(func_call_rule, True)]]
                )

p39 = Production(expr_list,
                [[expression, expr_separator, expr_list], [expression]],
                [[(expr_list_rule1, True)], [(expr_list_rule2, True)]]
                )

productions = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20,
                p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35, p36, p37, p38, p39]

orbsim_grammar = Grammar(terminals, non_terminals, program, productions)

orbsim_token_string: Dict[Token_Type, str] = {
    Token_Type.class_orbsim : 'class',
    Token_Type.let : 'let',
    Token_Type.if_orbsim : 'if',
    Token_Type.then : 'then',
    Token_Type.else_orbsim : 'else',
    Token_Type.loop : 'loop',
    Token_Type.break_orbsim : 'break',
    Token_Type.continue_orbsim : 'continue',
    Token_Type.func : 'func',
    Token_Type.return_orbsim : 'ret',
    Token_Type.print_orbsim : 'print',
    Token_Type.make_orbsim : 'make',
    
    Token_Type.int: 'int_val',
    Token_Type.float : 'float_val',
    Token_Type.boolean : 'boolean_val',
    Token_Type.string : 'string_val',
    Token_Type.id_orbsim : 'id_orbsim',
    Token_Type.type_id_orbsim : 'type_id',
    
    Token_Type.plus : '+',
    Token_Type.minus : '-',
    Token_Type.mul : '*',
    Token_Type.div : '/',
    Token_Type.mod : '%',

    Token_Type.neg : '!',
    Token_Type.logical_or: '||',
    Token_Type.logical_and: '&&',
    Token_Type.bitwise_or: '|',
    Token_Type.bitwise_xor: '^',
    Token_Type.bitwise_and: '&',
    Token_Type.bitwise_shift_left: '<<',
    Token_Type.bitwise_shift_right: '>>',

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
