from orbsim_language.ast_print_walk import PrintAST
from orbsim_language.orbsim_ast import IntegerNode, VariableDeclr, ProgramNode

printer = PrintAST()
number = IntegerNode(1)
number2 = IntegerNode(2)

let1 = VariableDeclr('a', number)
let2 = VariableDeclr('b', number2)
program = ProgramNode([let1, let2])

print(printer.visit(program))
