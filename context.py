# context.py
'''
Clase de alto nivel que contiene todo sobre el análisis/ejecución de un programa PL0.

Sirve como repositorio de información sobre el programa, incluido el código fuente, informe de errores, etc.
'''
#from interp  import Interpreter
from AST   import node
from plex    import Lexer
from pparse  import Parser


class Context:

  def __init__(self):
    self.lexer  = Lexer(self)
    self.parser = Parser()
    #self.interp = Interpreter(self)
    self.source = ''
    self.ast    = None
    self.have_errors = False

  def parse(self, source):
    self.have_errors = False
    self.source = source
    self.ast = self.parser.parse(self.lexer.tokenize(self.source))

  def run(self):
    if not self.have_errors:
      ...
      #checker.check()
      #return self.interp.interpret(self.ast)

  def find_source(self, node):
    indices = self.parser.index_position(node)
    if indices:
      return self.source[indices[0]:indices[1]]
    else:
      return f'{type(node).__name__} (fuente no disponible)'

  def error(self, message, position):
    if isinstance(position, node):
      lineno = self.parser.line_position(position)
      (start, end) = (part_start, part_end) = self.parser.index_position(position)
      if end == None:
        end = start
        part_end = start
      while start >= 0 and self.source[start] != '\n':
        start -=1
      while end < len(self.source) and self.source[end] != '\n':
        end += 1
      print()
      print(self.source[start:end])
      print(" "*(part_start - start), end='')
      print("^"*(part_end - part_start))
      print(f'{lineno}: {message}')

    else:
      print(f'{position}: {message}')

    self.have_errors = True

