#from AST import RenderAST
from plex import Lexer
import pathlib
from AST import *
from pparse import Parser
from dot import *
import sys
import rich
from typing import Any, List
Comentarios=[]




if len(sys.argv) !=2:
 print(f"Usage (sys.argv[0]) textfile")
 exit(1)

code = pathlib.Path(sys.argv[1]).read_text()

print (code)

lex = Lexer()

pas = Parser()

tokenize = lex.tokenize(code)

ast = pas.parse(tokenize)
print(ast)

render=RenderAST.render(ast)
print(render)

file_path = 'C:/Users/miguel/Desktop/miguelangel.trejos/Users/miguel/Desktop/plo2/dot'

with open(file_path, 'w') as file:
 file.write(render.source)

print(render)

