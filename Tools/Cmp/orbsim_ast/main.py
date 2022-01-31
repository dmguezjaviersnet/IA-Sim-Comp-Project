from ast_print_walk import PrintAST
from Integer_node import Integer_node
from variable_declr import VariableDeclr
from Tools.Cmp.Orbsim_AST.program_node import Program_node
from ast_print_walk import PrintAST

printer = PrintAST()
number = Integer_node(1)
number2 = Integer_node(2)

let1 = VariableDeclr('a', number)
let2 = VariableDeclr('b', number2)
program = Program_node([let1, let2])

print(printer.visit(program))
