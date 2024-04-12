

import argparse
from contextlib import redirect_stdout
from rich        import print as print2
from colorama import init, Fore, Back, Style
from plex       import pprint
from pparse     import gen_ast, print_ast
from plex       import *
from plex import *
from pparse import *
from plex import Lexer
from AST import *
from pparse import Parser
from checker import *

def parse_args():
  cli = argparse.ArgumentParser(
    prog='pl0.py',
    description='Compiler for PL0 programs')

  cli.add_argument(
    '-v', '--version',
    action='version',
    version='0.1')

  fgroup = cli.add_argument_group('Formatting options')

  fgroup.add_argument(
    'input',
    type=str,
    nargs='?',
    help='PL0 program file to compile')

  mutex = fgroup.add_mutually_exclusive_group()

  mutex.add_argument(
    '-l', '--lex',
    action='store_true',
    default=False,
    help='Store output of lexer')

  mutex.add_argument(
    '-d', '--dot',
    action='store_true',
    default=False,
    help='Generate AST graph as DOT format')

  mutex.add_argument(
    '-p', '--png',
    action='store_true',
    help='Generate AST graph as png format')

  mutex.add_argument(
    '-c', '--check',
    action='store_true',
    help='Check the program for errors')

  mutex.add_argument(
    '--sym',
    action='store_true',
    help='Dump the symbol table')


  mutex.add_argument(
    '-pAST', '--printAST',
    action='store_true',
    help='Print the AST')

  return cli.parse_args()


if __name__ == '__main__':

  args = parse_args()
  context = Context()

  if args.input: fname = args.input

  with open(fname, encoding='utf-8') as file:
    source = file.read()

  if args.lex:
    flex = fname.split('.')[0] + '.lex'
    print(f'print lexer: {flex}')
    with open(flex, 'w', encoding='utf-8') as f:
      with redirect_stdout(f):
        pprint(source)

  elif args.dot or args.png:
    '''Primero hacemos el checker para ver si hay errores, si no hay errores entonces generamos el AST y el dot'''
    context.parse(source)
    checker = Checker(context)
    checker.checker(context.ast,context)
    if context.have_errors:
      exit(1)

    ast, dot = gen_ast(source)
    base = fname.split('.')[0]
    if args.dot:
      fdot = base + '.dot'
      print(f'print ast: {fdot}')
      with open(fdot, 'w') as f:
        with redirect_stdout(f):
          print(dot)

    if args.pAST:
          print(dot)

    elif args.png:
      ...



    else:
      context.parse(source)
      context.run()

  elif args.check:
    context.parse(source)
    checker = Checker(context)
    checker.checker(context.ast,context)
    if context.have_errors == False:
      print("No hay errores!")

  elif args.sym:
    context.parse(source)
    checker = Checker(context)
    checker.symtab=checker.checker(context.ast,context)
    if context.have_errors == False:
      flex = fname.split('.')[0] + '.sym'
      print(f'print symbol table: {flex}')
      with open(flex, 'w', encoding='utf-8') as f:
        with redirect_stdout(f):
          checker.symtab.print_symbol_table()
    else:
      print("Hay errores en el programa, no se puede generar la tabla de simbolos")


  else:

    try:
      while True:
        source = input('pl0 $ ')
        context.parse(source)
        if not context.have_errors:
          for stmt in context.ast.funlist:
            context.ast = stmt
            context.run()

    except EOFError:
      pass

