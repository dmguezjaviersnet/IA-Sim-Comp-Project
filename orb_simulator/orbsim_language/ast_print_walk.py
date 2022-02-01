import visitor as visitor
from orbsim_ast.program_node import ProgramNode
from orbsim_ast.func_declr import*
from orbsim_ast.variable_declr import VariableDeclr
from orbsim_ast.atomic_node import AtomicNode

class PrintAST:

    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, tabs =0):
        ans = '\t' * tabs + f'-->*ProgramNode [<stat>; ... <stat>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'
    
    @visitor.when(FuncDeclr)
    def visit(self, node: FuncDeclr, tabs = 0):
        params = ', '.join(node.args)
        ans = '\t' * tabs + f'-->*FuncDeclarationNode: def {node.identifier}({params}) -> <expr>'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'

    @visitor.when(VariableDeclr)
    def visit(self, node: VariableDeclr, tabs = 0):
        ans = '\t' * tabs + f'-->*VarDeclarationNode: let {node.identifier} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(AtomicNode)
    def visit(self, node: AtomicNode, tabs = 0):
        return '\t' * tabs + f'-->*{node.__class__.__name__}: {node.val}'

        
        