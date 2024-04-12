from dataclasses import asdict
import sly
from AST import *
from plex import Lexer
from dot import *
import AST

class Parser(sly.Parser):
   # log = logging.getLogger()
    #log.setLevel(logging.ERROR)
    expected_shift_reduce = 1
    debugfile = 'pl0.txt'
    tokens = Lexer.tokens

    precedence =  (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'II', 'DI','MAI', 'MEI', '>', '<'),
        ('left', 'ADD', 'SUB'),
        ('left', 'MUL', 'DIV'),
        ('right', 'NOT'),
        ('nonassoc', 'THEN'),
        ('nonassoc', 'ELSE'),
    )

    # Implementacion Reglas de la Gramatica

    @_("funclist")
    def program(self, p):
        return Program(p.funclist)

    @_("funclist function" )
    def funclist(self, p):
        return p.funclist + [p.function]

    @_("function")
    def funclist(self, p):
        return [p.function]

    @_("FUN NAME '(' [ arglist ] ')' [ locals ] BEGIN statements END")
    def function(self, p):
        function_name = p.NAME
        arguments = p.arglist
        locals = p.locals
        statements = p.statements

        return Function(function_name, arguments, locals, statements,None)

    @_("statements ';' statement")
    def statements(self, p):
        return p.statements + [p.statement]

    @_("statement")
    def statements(self, p):
        return [p.statement]

    @_("WHILE relation DO statement")
    def statement(self, p):
        return While(p.relation, p.statement)

    @_("FOR NAME ASIG expr TO expr DO statement")
    def statement(self, p):
        A=Assing(SimpleLocation(p.NAME,None), p.expr0,None)
        B=While(Relation("<=",SimpleLocation(p.NAME,None), p.expr1,None), Begin([p.statement,Assing(SimpleLocation(p.NAME,None), Binary("+", SimpleLocation(p.NAME,None), Integer(1,SimpleType("int")),None),None)]))
        return Begin([A,B])

    @_("FOR NAME ASIG expr DOWNTO expr DO statement")
    def statement(self,p):
        A=Assing(SimpleLocation(p.NAME,None), p.expr0,None)
        B=While(Relation(">=", SimpleLocation(p.NAME,None), p.expr1,None), Begin([p.statement,Assing(SimpleLocation(p.NAME,None), Binary("-", SimpleLocation(p.NAME,None), Integer(1,SimpleType("int")),None),None)]))
        return Begin([A,B])

    @_("IF relation THEN statement ELSE statement %prec ELSE")
    def statement(self, p):
        return If(p.relation, p.statement0, p.statement1)

    @_("IF relation THEN statement %prec THEN")
    def statement(self, p):
        return If(p.relation, p.statement, None)

    @_("location ASIG expr")
    def statement(self, p):
        return Assing(p.location, p.expr,None)

    @_("PRINT '(' LITERAL ')'")
    def statement(self, p):
        return Print(p[2])

    @_("WRITE '(' expr ')'")
    def statement(self, p):
        return Write(p.expr, None)

    @_("READ '(' location ')'")
    def statement(self, p):
        return Read(p.location, None)

    @_("RETURN expr")
    def statement(self, p):
        return Return(p.expr, None)

    @_("NAME '(' exprlist ')'")
    def statement(self, p):
        return FunCall(p[0], p[2],None )

    @_("SKIP")
    def statement(self, p):
        return Skip()

    @_("BREAK")
    def statement(self, p):
        return Break()

    @_("BEGIN statements END")
    def statement(self, p):
        return Begin(p.statements)

    @_("expr ADD expr",
       "expr SUB expr",
       "expr MUL expr",
       "expr DIV expr")
    def expr(self, p):
        return Binary(p[1], p[0], p[2],None)

    @_("SUB expr",
       "ADD expr")
    def expr(self, p):
        return Unary(p[0], p.expr,None)

    @_( "'(' expr ')'")
    def expr(self, p):
        return p.expr

    @_("NAME '[' expr ']'")
    def expr(self, p):
        return ArrayLocation(p[0], p[2],None)

    @_("NAME '(' exprlist ')'")
    def expr(self, p):
        return FunCall(p[0], p[2],None)

    @_("NAME")
    def expr(self, p):
        return SimpleLocation(p[0],None)

    @_("INT")
    def expr(self, p):
        return Integer(p[0],SimpleType("int"))

    @_("FLOAT")
    def expr(self, p):
        return Float(p[0],SimpleType("float"))

    @_("INT_T '(' expr ')'",
       "FLOAT_T '(' expr ')'")
    def expr(self, p):
        return TypeCast(p[0], p[2])

    @_(" exprlist ',' expr ")
    def exprlist(self, p):
        return p.exprlist + [p.expr]

    @_("expr",)
    def exprlist(self, p):
        return [p.expr]

    @_("")
    def exprlist(self, p):
        return []

    @_("expr '<' expr",
       "expr '>' expr",
       "expr MEI expr",
       "expr MAI expr",
       "expr II expr",
       "expr DI expr")
    def relation(self, p):
        return Relation(p[1], p[0], p[2],None)

    @_("relation AND relation",
       "relation OR relation")
    def  relation(self, p):
        return Relation(p[1], p[0], p[2],None)

    @_("NOT relation ")
    def  relation(self, p):
        return Relation(p[0], p[1], None, None)

    @_("'(' relation ')'")
    def  relation(self, p):
        return p.relation

    @_("NAME ':'  INT_T [ '[' expr ']' ]",
       "NAME ':'  FLOAT_T [ '[' expr ']' ]")
    def  arg(self, p):
        if p.expr != None:
           return Argument(p[0], ArrayType(p[2], p.expr))
        else:
              return Argument(p[0], SimpleType(p[2]))

    @_("arglist ',' arg")
    def  arglist(self, p):
        return p.arglist + [p.arg]

    @_("arg")
    def  arglist(self, p):
        return [p.arg]

    @_("locals arg ';' ",
       "locals function ';'")
    def locals(self, p):
        return p.locals + [p[1]]

    @_("arg ';' ",
       "function ';'")
    def locals(self, p):
        return [p[0]]

    @_("NAME")
    def location(self, p):
        return SimpleLocation(p[0],None)

    @_("NAME '[' expr ']'")
    def location(self, p):
        return ArrayLocation(p[0], p[2],None)


    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type} ({p.value}) in line {p.lineno}")
        else:
            print("Syntax error at EOF")

def gen_ast(argv):

    lex = Lexer()
    pas = Parser()


    ast = pas.parse(lex.tokenize(argv))
    return ast , RenderAST.render(argv,ast)



def print_ast(node, indent=0):

  if indent == 0:
    print(":::: Parse Tree ::::")

  print("  " * indent, end="")

  if isinstance(node, Program):
    print("program")

  else:
    print("+-- " + type(node).__name__)

  for name, value in vars(node).items():

    if isinstance(value, AST.node):
      print_ast(value, indent + 2)

    elif isinstance(value, list):
      for item in value:
        print_ast(item, indent + 2)

    else:
      print("  " * (indent + 2), end="")
      print("|-- " + name, end="")
      print(" (" + str(value) + ")")