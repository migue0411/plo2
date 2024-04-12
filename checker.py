
from AST import *
from typesys import *
from context import *
from colorama import init, Fore, Back, Style


class Symtab:

    class SymbolDefinedError(Exception):
        pass

    def __init__(self, parent=None, name=None, lineno=0, Return=False):
        self.name = name
        self.entries = {}
        self.parent = parent
        self.bealoop = False
        self.Return = Return
        self.lieneo = lineno
        if self.parent:
            self.parent.children.append(self)
        self.children = []

    def haveReturn(self):
        self.Return = True

    def checkReturn(self):
        for child in self.children:
            child.checkReturn()
        if not self.Return:
            print("\x1b[1;31m"+self.name+"\x1b[0;31m"+f" no tiene almenos un return, linea: {self.lieneo}"+Fore.RESET )
            # print( "no: ",self.name)
        return False

    def printenv(self):
        for child in self.children:
            child.printenv()
        print(" ", self.name, ": ")
        for i in self.entries:
            print("   ", i, "-", self.entries[i])

    def iamaloop(self):
        self.bealoop = True

    def add(self, str, value):
        if str in self.entries:
            raise Symtab.SymbolDefinedError()
        self.entries[str] = value

    def amialoop(self):
        if self.bealoop:
            return True
        elif self.parent:
            return self.parent.amialoop()
        return False

    def get(self, name):
        if name in self.entries:
            return self.entries[name]
        elif self.parent:
            return self.parent.get(name)
        return None


class Checker(Visitor):
    def __init__(self,context):
        self.context=context
        self.error = context.error
        self.context.have_errors = False
        self.whileBool=False
        self.funcall=False
        self.symtab=Symtab()
    @classmethod
    def checker(cls, n:node, context:Context):
        c=cls(context)
        return n.accept(c, Symtab())

    def visit(self, n: Program, env: Symtab):
        # Crear un nuevo contexto (Symtab global)
        Table = Symtab()
        # Visitar cada una de las declaraciones asociadas
        for funt in n.funlist:
            funt.accept(self, Table)
        self.symtab=Table
        if(Table.get('main') == None):
            self.context.error('No se encuentra la funcion main', 0)
            self.context.have_errors=True
        return Table


    def visit(self, n: Function, env: Symtab):
        # Agregar el nombre de la funcion a Symtab
        if env.add(n.name, n):
            self.context.error(f'La funcion {n.name} ya esta declarada', n)
            self.context.have_errors=True
        # Crear un nuevo contexto (Symtab)
        Table = Symtab(env)
        # Visitar ParamList
        if n.arguments != None:
            for arg in n.arguments:
                arg.accept(self, Table)

        # Visitar VarList
        if n.locals != None:
            for local in n.locals:

                local.accept(self, Table)

        # Visitar StmtList
        datatype=None
        if n.statements != None:

            for stmt in n.statements:
                stmt.accept(self, Table)
                 # Determinar el datatype de la funcion (revisando instrucciones return)
                if isinstance(stmt, Return):
                    datatype=stmt.datatype
                    n.datatype=datatype

        return datatype

    def visit(self, n: Name, env: Symtab):
        # Buscar el nombre en Symtab
        nombre=env.get(n.name)
        if nombre == None:
            self.context.error(f'No se encuentra {n.name}',n)
            self.context.have_errors=True

    def visit(self, n: Literal, env: Symtab):
        # Devolver datatype
        return n.datatype.name

    def visit(self, n: Location, env: Symtab):
        # Buscar en Symtab y extraer datatype (No se encuentra?)
        node = env.get(n.name)
        if node == None:
            self.context.error(f'No se encuentra {n.name}',n)
            self.context.have_errors=True
        elif isinstance(n, ArrayLocation):
            errors=False
            dattype=n.expr.accept(self, env)
            if dattype != 'int':
                self.context.error(f'El indice del array {n.name} no es un entero',n)
                self.context.have_errors=True
                errors=True

            if isinstance(node.datatype, SimpleType) and self.funcall==False :
                self.context.error(f' {n.name} es una variable, no un array',n)
                self.context.have_errors=True
                errors=True
            if errors==False:
                n.datatype=node.datatype
                return node.datatype.name
        elif isinstance(n, SimpleLocation) :
            if isinstance(node.datatype, ArrayType)and self.funcall==False:
                self.context.error(f' {n.name} es un array, no una variable',n)
                self.context.have_errors=True
            else:
                n.datatype=node.datatype
                return node.datatype.name
        else:
            # Devuelvo el datatype
            n.datatype=node.datatype
            return node.datatype.name

    def visit(self, n: TypeCast, env: Symtab):
        # Visitar la expresion asociada
        n.expr.accept(self, env)
        # Devolver datatype asociado al nodo
        return n.datatype


    def visit(self, n: FunCall, env: Symtab):
        self.funcall=True
        # Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
        node = env.get(n.name)
        #Tipo de retorno
        if node == None:
            self.context.error(f'No se encuentra  {n.name}  declarada o esta declarada de forma local en otra funcion ',n)
            self.context.have_errors=True
        elif not isinstance(node, Function):
            self.context.error(f'{n.name} no es una funcion',n)
        else:
            datatype=node.datatype
            #Num Parametros
            NumParm=len(node.arguments)
            # Visitar la lista de Argumentos
            listdtype=[]
            listargument=[]
            listantype=[]
            if n.exprlist != None:
                for arg in n.exprlist:
                    listdtype.append(arg.accept(self, env))
                    if  isinstance(arg, SimpleLocation) or  isinstance(arg,ArrayLocation):
                        # Buscar la Variable en Symtab
                        nodo=env.get(arg.name)
                        if isinstance(nodo.datatype, ArrayType):
                            listargument.append(nodo.datatype.expr.value)
                        else:
                            listargument.append(None)
                        listantype.append(arg)
                    else:
                        listargument.append(None)
                        listantype.append(arg)
            if n.exprlist == None:
                self.context.error(f'Numero de argumentos incorrecto',n)
                self.context.have_errors=True
            else:
                # Comparar el numero de argumentos con parametros
                if NumParm != len(n.exprlist):
                    self.context.error(f'Numero de argumentos incorrecto',n)
                    self.context.have_errors=True
                else:
                    # Comparar cada uno de los tipos de los argumentos con los parametros
                    j=0
                    for i in node.arguments:
                        if i.datatype.name != listdtype[j]:
                            self.context.error(f'El tipo de dato del para el parametro {i.name} es incorrecto. Tiene {listdtype[j]} y se esperaba {i.datatype.name}. En llamado de la funcion {n.name}', n)
                            self.context.have_errors=True

                        if isinstance(i.datatype, ArrayType) :
                            if i.datatype.expr.value != listargument[j]:
                                if listargument[j] == None:
                                    self.context.error(f"En el parametro  {i.name} no se le ingreso un tipo de dato array",n)
                                else:
                                    self.context.error(f"El Tamaño del Array para el parametro  {i.name} es incorrecto. Envia un tamaño de {listargument[j]} y se esperaba {i.datatype.expr.value}. En llamado de la funcion {n.name}",n)
                                self.context.have_errors=True
                            elif  isinstance(listantype[j], ArrayLocation):
                                self.context.error(f"El parametro {i.name} es un array. No le esta enviando un array",n)
                                self.context.have_errors=True
                        elif isinstance(i.datatype, SimpleType):
                            if len(listargument) !=0:
                                if listargument[j] != None and isinstance(listantype[j], SimpleLocation):
                                    self.context.error(f"El parametro {i.name} es una variable. No le esta enviando una variable",n)
                                    self.context.have_errors=True
                        j+=1
                    self.funcall=False
                    # Retornar el datatype de la funcion
                    n.datatype=datatype
                    return datatype

    def visit(self, n: Binary, env: Symtab):

        # Visitar el hijo izquierdo (devuelve datatype)
        izq = n.left.accept(self, env)
        # Visitar el hijo derecho (devuelve datatype)
        der = n.right.accept(self, env)
        # Comparar ambos tipo de datatype
        if isinstance(der,SimpleType):
            der=der.name
        if isinstance(izq,SimpleType):
            izq=izq.name
        datatype=check_binary_op(n.op, izq, der)
        if datatype == None:
            self.context.error(f'No se puede operar {izq} con {der}',n)
            self.context.have_errors=True
        else:
            n.datatype=SimpleType(datatype)
            return datatype

    def visit(self, n: Relation, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        izq=n.left.accept(self, env)
        # Visitar el hijo derecho (devuelve datatype)
        der=n.right.accept(self, env)
        # Comparar ambos tipo de datatype
        if isinstance(der,SimpleType):
            der=der.name
        if isinstance(izq,SimpleType):
            izq=izq.name
        datatype=check_binary_op(n.op, izq, der)
        if datatype == None:
            self.context.error(f'No se puede operar {izq} con {der}',n)
            self.context.have_errors=True
        else:
            n.datatype=datatype
            return datatype

    def visit(self, n: Unary, env: Symtab):
        # Visitar la expression asociada (devuelve datatype)
        data_type_expr=n.expr.accept(self, env)
        # Comparar datatype
        if isinstance(data_type_expr,SimpleType):
            data_type_expr=data_type_expr.name
        datatype=check_unary_op(n.op, data_type_expr)
        if datatype == None:
            self.context.error(f'No se puede operar {data_type_expr}',n)
            self.context.have_errors=True
        else:
            n.datatype=datatype
            return datatype

    def visit(self, n: Argument, env: Symtab):
        # Agregar el nombre del parametro a Symtab
        if env.add(n.name, n):
            self.context.error(f'El parametro {n.name} ya esta declarado',n)
            self.context.have_errors=True
        else:
            return n.datatype

    def visit(self, n: Print, env: Symtab):
        ...

    def visit(self, n: Write, env: Symtab):
        n.expr.accept(self, env)
        # Buscar la Variable en Symtab
        if isinstance(n.expr, SimpleLocation) or isinstance(n.expr, ArrayLocation):
            nodo=env.get(n.expr.name)
            if nodo == None:
                self.context.error(f'No se encuentra {n.expr.name}',n)
                self.context.have_errors=True
            elif  nodo.datatype==None:
                self.context.error(f'Tipo de retorno desconocido de {n.expr.name} ',n)
                self.context.have_errors=True
            else:
                n.datatype=nodo.datatype
                return nodo.datatype.name
        if isinstance(n.expr, Literal):
            n.datatype=n.expr.datatype
            return n.expr.datatype.name

    def visit(self, n: Read, env: Symtab):
        n.local.accept(self, env)
        # Buscar la Variable en Symtab
        nodo=env.get(n.local.name)
        if nodo == None:
            self.context.error(f'No se encuentra {n.local.name}',n)
            self.context.have_errors=True
        else:
            n.datatype=nodo.datatype
            return nodo.datatype.name

    def visit(self, n: While, env: Symtab):
        self.whileBool=True
        # Visitar la condicion del While (Comprobar tipo bool)
        condition_type = n.relation.accept(self, env)
        if condition_type != 'bool':
            self.context.error(f'Tipo incorrecto para la condición del While. Se esperaba "bool", pero se encontró "{condition_type}".',n)
            self.context.have_errors=True
        # Visitar las Stmts
        n.statement.accept(self, env)
        self.whileBool=False

    def visit(self, n: Break, env: Symtab):
        # Esta dentro de un While?
        if self.whileBool == False:
            self.context.error('La instrucción "Break" debe estar dentro de un bucle "While".',n)
            self.context.have_errors=True

    def visit(self, n: If, env: Symtab):
        # Visitar la condicion del IfStmt (Comprobar tipo bool)
        condition_type = n.relation.accept(self, env)
        if condition_type != 'bool':
            self.context.error(f'Tipo incorrecto para la condición del If. Se esperaba bool, pero se encontró {condition_type}',n)
            self.context.have_errors=True
        # Visitar las Stmts del then
        n.statement.accept(self, env)

        # Visitar las Stmts del else, si existen
        if n.if_else is not None:
            n.if_else.accept(self, env)


    def visit(self, n: Return, env: Symtab):

        padre=list(env.parent.entries.keys())
        nombre_funcion=padre[len(padre)-1] #Nombre de la funcion
        nodo_funcion=env.get(nombre_funcion)
        # Visitar la expresion asociada
        expr_type = n.expr.accept(self, env)
        # Actualizar el datatype de la funcion
        nodo_funcion.datatype=SimpleType(expr_type)
        n.datatype = SimpleType(expr_type)
        return expr_type


    def visit(self, n: Skip, env: Symtab):
        ...

    def visit(self, n: Begin, env: Symtab):
        # Visitar cada una de las instruciones asociadas
        for stmt in n.statements:
            stmt.accept(self, env)

    def visit(self, n: Assing, env:Symtab):
         # Buscar la Variable en Symtab
        nodo=env.get(n.location.name)
        n.location.accept(self, env)



        if nodo == None:
            self.context.error(f'No se encuentra {n.location.name}',n)
            self.context.have_errors=True
        else:

            expr_type = n.expr.accept(self, env)

            if isinstance(expr_type,SimpleType):
                expr_type=expr_type.name
            dataType= check_binary_op('+', nodo.datatype.name, expr_type)
            if dataType == None:
                self.context.error(f'No se puede asignar {expr_type} a {nodo.datatype.name}',n)
                self.context.have_errors=True
            elif isinstance(nodo.datatype, ArrayType):
                if isinstance(n.location, SimpleLocation):
                    self.context.error(f'{n.location.name} es de tipo array, no se le puede asignar un valor a un array  ',n)
                    self.context.have_errors=True
                elif isinstance(n.location, ArrayLocation):
                    if isinstance(n.location.expr, Unary):
                        if n.location.expr.op== '-':
                            self.context.error(f'El indice del array {n.location.name} no puede ser negativo  ',n)
                            self.context.have_errors=True
            else:
                n.datatype=SimpleType(dataType)
                return dataType