from typing import List
from parser.lr1_parser import lr1_parse
from orbsim_language.orbsim_lexer import orbsim_lexer
from orbsim_language.orbsim_grammar import orbsim_grammar, orbsim_token_string

from orbsim_language.type_collector import TypeCollector
from orbsim_language.type_builder import TypeBuilder
from orbsim_language.type_checker import TypeChecker
from orbsim_language.executor import Executor
from orbsim_language.context import Scope

def orbsim_compile_and_execute(text: str):

    tokens, errs = orbsim_lexer(text)
    if errs:
        return errs
    errs, ast = lr1_parse(orbsim_grammar, tokens, orbsim_token_string)
    if errs:
        return errs
    collector = TypeCollector()
    collector.visit(ast)
    builder = TypeBuilder(collector.context, collector.log)
    builder.visit(ast)
    checker =  TypeChecker(builder.context, builder.log)
    checker.check(ast, Scope())
    if checker.log:
        return checker.log
    exe =  Executor(checker.context)
    exe.execute(ast, Scope())
    
    
# orbsim_compile_and_execute('''
# func Int fib(Int n){
#     if (n == 1 || n == 0) then {
#         ret 1;
#     }
#     else{
#         ret fib(n-1) + fib(n-2);
#     };
# };

# let Int f = fib(5);
# print(f);

# ''')


