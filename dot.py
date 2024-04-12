import graphviz as gpv
from AST import *
class RenderAST(Visitor):
    node_default = {
        'shape' : 'box',
        'color' : 'deepskyblue',
        'style' : 'filled'
    }
    edge_default = {
        'arrowhead' : 'none',
    }

    def __init__(self,source):
        self.source = source
        self.dot = gpv.Digraph('AST')
        self.dot.attr('node', **self.node_default)
        self.dot.attr('edge', **self.edge_default)
        self.seq = 0


    def __str__(self):
        return self.dot.source

    def __repr__(self):
        return self.dot.source

    def name(self):
        self.seq += 1
        return f'n{self.seq:0d}'

    @classmethod
    def render(cls, source ,n:node):
        dot = cls(source)
        n.accept(dot)
        return dot.dot

    def visit(self, n:Program):
        name = self.name()
        self.dot.node(name, label='Program')
        for funt in n.funlist:
            self.dot.edge(name, funt.accept(self))

    def visit(self, n:Function):
        name = self.name()
        self.dot.node(name, label=f'FuncDefinition\n{n.name}')
        if n.arguments != None:
            arg_name = self.name()
            self.dot.node(arg_name, label='ArgList')
            for arg in n.arguments:
                self.dot.edge(arg_name, arg.accept(self))
            self.dot.edge(name, arg_name)
        if n.locals != None:
            local_name = self.name()
            self.dot.node(local_name, label='LocalsList')
            for local in n.locals:
                self.dot.edge(local_name, local.accept(self))
            self.dot.edge(name, local_name)
        if n.statements != None:
            stmt_name = self.name()
            self.dot.node(stmt_name, label='StmtList')
            for stmt in n.statements:
                self.dot.edge(stmt_name, stmt.accept(self))
            self.dot.edge(name, stmt_name)
        return name

    def visit(self, n:Name):
        return n.name

    def visit(self, n:Integer):
        name = self.name()
        self.dot.node(name, label=f'Integer\n{n.value}', color='chartreuse')
        return name

    def visit(self, n:Float):
        name = self.name()
        self.dot.node(name, label=f'Float\n{n.value}', color='chartreuse')
        return name

    def visit(self, n:Relation):
        name = self.name()
        self.dot.node(name, label=f'{n.op}', color='darkgoldenrod', shape='circle')
        self.dot.edge(name, n.left.accept(self))
        self.dot.edge(name, n.right.accept(self))
        return name

    def visit(self, n:Assing):
        name = self.name()
        self.dot.node(name, label=f'Assign')
        self.dot.edge(name, n.location.accept(self))
        self.dot.edge(name, n.expr.accept(self))
        return name

    def visit(self, n:Print):
        name = self.name()
        self.dot.node(name, label=f'Print\n{n.string}')
        return name

    def visit(self, n:Write):
        name = self.name()
        self.dot.node(name, label=f'Write')
        self.dot.edge(name, n.expr.accept(self))
        return name

    def visit(self, n:Read):
        name = self.name()
        self.dot.node(name, label=f'Read')
        self.dot.edge(name, n.local.accept(self))
        return name

    def visit(self, n:While):
        name = self.name()
        self.dot.node(name, label=f'While')
        self.dot.edge(name, n.relation.accept(self))
        self.dot.edge(name, n.statement.accept(self))
        return name

    def visit(self, n:If):
        name = self.name()
        self.dot.node(name, label=f'IfStmt')
        self.dot.edge(name, n.relation.accept(self))
        self.dot.edge(name, n.statement.accept(self))
        if n.if_else != None:
            self.dot.edge(name, n.if_else.accept(self))
        return name

    def visit(self, n:Return):
        name = self.name()
        self.dot.node(name, label=f'Return')
        self.dot.edge(name, n.expr.accept(self))
        return name

    def visit(self,n:Skip):
        name = self.name()
        self.dot.node(name, label=f'Skip')
        return name

    def visit(self,n:Break):
        name = self.name()
        self.dot.node(name, label=f'Break')
        return name

    def visit(self, n:Begin):
        name = self.name()
        self.dot.node(name, label=f'Begin \nStmtList')
        for stmt in n.statements:
            self.dot.edge(name, stmt.accept(self))
        return name

    def visit(self, n:SimpleType):
        name = self.name()
        self.dot.node(name, label=f'SimpleType \n{n.name}')
        return name

    def visit(self, n:ArrayType):
        name = self.name()
        self.dot.node(name, label=f'ArrayType \n{n.name}')
        self.dot.edge(name, n.expr.accept(self))
        return name

    def visit(self, n:SimpleLocation):
        name = self.name()
        self.dot.node(name, label=f'SimpleLocation \n{n.name}', color='chartreuse')
        return name

    def visit(self, n:ArrayLocation):
        name = self.name()
        self.dot.node(name, label=f'ArrayLocation \n{n.name}', color='chartreuse')
        self.dot.edge(name, n.expr.accept(self))
        return name

    def visit(self, n:Literal):
        name = self.name()
        self.dot.node(name, label=f'Literal\n{n.value}', color='chartreuse')
        return name

    def visit(self, n:Binary):
        name = self.name()
        self.dot.node(name, label=f'{n.op}', color='darkgoldenrod', shape='circle')
        self.dot.edge(name, n.left.accept(self))
        self.dot.edge(name, n.right.accept(self))
        return name

    def visit(self, n:Unary):
        name = self.name()
        self.dot.node(name, label=f'{n.op}', color='darkgoldenrod', shape='circle')
        self.dot.edge(name, n.expr.accept(self))
        return name

    def visit(self, n:Argument):
        name = self.name()
        if type(n.datatype) == SimpleType:
            self.dot.node(name, label=f'Argument\n {n.name}:{n.datatype.name}', color='chartreuse')
        else:
            self.dot.node(name, label=f'Argument\n {n.name}:{n.datatype.name}[{n.datatype.expr.value}]', color='chartreuse')
        return name

    def visit(self, n:TypeCast):
        name = self.name()
        self.dot.node(name, label=f'{n.datatype.name}')
        self.dot.edge(name, n.expr.accept(self))
        return name

    def visit(self, n:FunCall):
        name = self.name()
        self.dot.node(name, label=f'FunCall ({n.name})')
        name_arg = self.name()
        self.dot.node(name_arg, label='ArgList', shape='point')
        for expr in n.exprlist:
            self.dot.edge(name_arg, expr.accept(self))
        self.dot.edge(name, name_arg)
        return name