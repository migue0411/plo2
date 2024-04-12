

from dataclasses import dataclass,field
from multimethod import multimeta
import graphviz as gpv
from typing import Any, List
from plex import *
from dataclasses import dataclass
from multimethod import multimeta
import pydot

class Visitor(metaclass=multimeta):
  ...

@dataclass
class node:
  def accept(self, v:Visitor, *args, **kwargs):
    return v.visit(self, *args, **kwargs)

@dataclass
class Statement(node):
    ...

@dataclass
class DataType(node):
    ...

@dataclass
class Location(node):
    ...

@dataclass
class Expression(node):
    ...

@dataclass
class Program (Statement):
    funlist: list

@dataclass
class Declaration(Statement):
    ...

@dataclass
class Name(Expression):
    name: str

@dataclass
class Literal(Expression):
    ...

@dataclass
class Relation(Expression):
    op: str
    left: Expression
    right: Expression
    datatype: DataType

@dataclass
class Function(Declaration):
    name: Name
    arguments: list
    locals: list
    statements: list
    datatype: DataType

@dataclass
class Assing(Statement):
    location: Location
    expr: Expression
    datatype:DataType

@dataclass
class Print(Statement):
    string: str

@dataclass
class Write(Statement):
    expr: Expression
    datatype: DataType

@dataclass
class Read(Statement):
    local:Location
    datatype: DataType

@dataclass
class While(Statement):
    relation: Relation
    statement: Statement

@dataclass
class If(Statement):
    relation: Relation
    statement: Statement
    if_else : Statement

@dataclass
class Return(Statement):
    expr: Expression
    datatype: DataType

@dataclass
class Skip(Statement):
    ...

@dataclass
class Break(Statement):
    ...

@dataclass
class Begin(Statement):
    statements: list

@dataclass
class SimpleType(DataType):
    name: Name


@dataclass
class ArrayType(DataType):
    name: Name
    expr: Expression


@dataclass
class SimpleLocation(Location):
    name: Name
    datatype: DataType

@dataclass
class ArrayLocation(Location):
    name: Name
    expr: Expression
    datatype: DataType

@dataclass
class String(Expression):
    cadena: str

@dataclass
class Binary(Expression):
    op: str
    left: Expression
    right: Expression
    datatype: DataType

@dataclass
class Unary(Expression):
    op: str
    expr: Expression
    datatype: DataType

@dataclass
class Argument(Declaration):
    name: Name
    datatype: DataType

@dataclass
class TypeCast(Expression):
    datatype: DataType
    expr: Expression

@dataclass
class FunCall(Expression):
    name: Name
    exprlist: list
    datatype: DataType

@dataclass
class Integer(Literal):
    value: int
    datatype: SimpleType(Name("int"))

@dataclass
class Float(Literal):
    value: float
    datatype: SimpleType(Name("float"))





# ----------------------------------------
# Expression representan valores
#


