# typesys.py
'''
Tipos del sistema
=================
Este archivo implementa características básicas del sistema de tipos. Aquí hay mucha flexibilidad posible, pero la mejor estrategia podría ser no pensar demasiado en el problema. Al menos no al principio. Estos son los requisitos básicos mínimos:

1. Los tipos tienen identidad (por ejemplo, como mínimo un nombre como 'int', 'float', etc.)
2. Los tipos tienen que ser comparables. (por ejemplo, int != flotante).
3. Los tipos admiten diferentes operadores (p. ej., +, -, *, /, etc.)

Una forma de lograr todos estos objetivos es comenzar con algún tipo de enfoque basado en tablas. No es lo más sofisticado, pero funcionará como punto de partida.
Puedes regresar y refactorizar el sistema de tipos más tarde.
'''

# Set of valid typenames
typenames = { 'int', 'float', 'bool' }

# Table of all supported binary operations and result types
_binary_ops = {
  # Integer operations
  ('+', 'int', 'int') : 'int',
  ('-', 'int', 'int') : 'int',
  ('*', 'int', 'int') : 'int',
  ('/', 'int', 'int') : 'int',

  ('<', 'int', 'int') : 'bool',
  ('<=', 'int', 'int'): 'bool',
  ('>', 'int', 'int') : 'bool',
  ('>=', 'int', 'int'): 'bool',
  ('==', 'int', 'int'): 'bool',
  ('!=', 'int', 'int'): 'bool',


  # Float operations
  ('+', 'float', 'float') : 'float',
  ('-', 'float', 'float') : 'float',
  ('*', 'float', 'float') : 'float',
  ('/', 'float', 'float') : 'float',

  ('<', 'float', 'float')  : 'bool',
  ('<=', 'float', 'float') : 'bool',
  ('>', 'float', 'float')  : 'bool',
  ('>=', 'float', 'float') : 'bool',
  ('==', 'float', 'float') : 'bool',
  ('!=', 'float', 'float') : 'bool',


  # Bool operations
  ('and', 'bool', 'bool') : 'bool',
  ('or', 'bool', 'bool') : 'bool',
  ('==', 'bool', 'bool') : 'bool',
  ('!=', 'bool', 'bool') : 'bool',

}

_unary_ops = {
  # Integer operations
  ('+', 'int') : 'int',
  ('-', 'int') : 'int',

  # Float operations
  ('+', 'float') : 'float',
  ('-', 'float') : 'float',

  # Bool operations
  ('not', 'bool') : 'bool',
}

def lookup_type(name):
  # Given the name of a primitive type, this looks up the
  # appropriate "type" object here.  For starting out, types are
  # just names, but later on they could be more advanced objects.
  if name in typenames:
    return name
  else:
    return None

def check_binary_op(op, left, right):
  # Check if a binary operation is allowed or not.  Returns the
  # result type or None if not supported.
  return _binary_ops.get((op, left, right))

def check_unary_op(op, expr):
  # Check if a unary operation is allowed or not. Returns the result
  # type or None if not supported.
  return _unary_ops.get((op, expr))

