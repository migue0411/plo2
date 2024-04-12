
import sly
import rich
Comentarios=[]
import sly
from rich.console import  Console
from rich.table import Table


class Lexer(sly.Lexer):
    tokens = {
        #Operadores
        ADD, SUB, MUL, DIV,
        #Palabras Reservadas
        FUN, BEGIN, END, WHILE, DO, IF, THEN, ELSE,
        PRINT, WRITE, READ, RETURN, SKIP, BREAK, INT_T,
        FLOAT_T,TO,DOWNTO, FOR,
        #Asignn (:=)
        ASIG,

        #Operadores de Relacion (MEI = Menor igual <=) (MAI = Mayor igual >=) (II = Igual igual ==) (DI = Diferente igual !=)
        AND, OR, NOT, MEI, MAI, II, DI,

        #Literales
        INT, FLOAT, NAME, LITERAL,
    }
    literals = '()[],.;:<>"'
    ignore = ' \t'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'(/\*(.|\n)*?\*/)')
    def ignore_comment(self,t):
        self.lineno += t.value.count('\n')

    @_(r'/\*(.|\n)+')
    def ignore_untermcomment(self,t):
        print(f"Line {self.lineno}. Unterminated comment.")
        self.lineno += t.value.count('\n')

    @_(r'[0]\d+.*')
    def numbers_error(self,t):
        print(f"Line {self.lineno}. Numero mal escrito {t.value}")
        self.lineno += t.value.count('\n')

    #Operadores
    ADD = r'\+'
    SUB = r'-'
    MUL = r'\*'
    DIV = r'/'

    @_(r'(\+|-)?([0]|[1-9][0-9]*)(\.[0-9]+((e|E)(\+|-)?[0-9]+)?|(e|E)(\+|-)?[0-9]+)')
    def FLOAT(self,t):
        t.value = float(t.value)
        return t

    @_(r'((\+|-)?[1-9][0-9]*)|[0]')
    def INT(self,t):
        t.value = int(t.value)
        return t

    @_(r'".*\\e.*"')
    def error_escape(self,t):
        print(f"Line {self.lineno}. Caracter de escape ilegal en {t.value}")
        self.lineno += t.value.count('\n')

    @_(r'".*[^(\\|\n)]"')
    def LITERAL(self,t):
        length=len(t.value)
        i=0
        sentence=0
        cadena="\""
        while (i<length):
            if t.value[i] == "\"" and t.value[i-1] != "\\" and sentence==0:
                sentence=1
            elif t.value[i] == "\"" and t.value[i-1] != "\\" and sentence == 1:
                sentence=0
            elif sentence==1:
                cadena=cadena+t.value[i]
            i+=1
        t.value=cadena+"\""
        return t



    @_(r'".*\n')
    def ignore_unterstring(self,t):
        print(f"Line {self.lineno}. Unterminated string.")
        self.lineno += t.value.count('\n')

    @_(r'\d+[a-zA-Z_]+')
    def identifier_error(self,t):
        print(f"Line {self.lineno}. Nombre de la funcion o variable mal escrito {t.value}")
        self.lineno += t.value.count('\n')

    MEI    =r'<='
    MAI    =r'>='
    II     =r'=='
    DI     =r'!='
    TO = r'[Tt][Oo]\b'
    DOWNTO = r'[Dd][Oo][Ww][Nn][Tt][Oo]\b'
    FOR = r'[Ff][Oo][Rr]\b'
    WHILE = r'[Ww][Hh][Ii][Ll][Ee]\b'
    ASIG   =r':='
    NOT    =r'[Nn][oO][Tt]\b'
    FUN    = r'[Ff][uU][Nn]\b'
    READ   = r'[rR][eE][aA][dD]\b'
    WRITE   = r'[wW][rR][iI][Tt][eE]\b'
    PRINT  = r'[Pp][Rr][Ii][Nn][Tt]\b'
    DO   = r'[Dd][Oo]\b'
    IF     = r'[iI][fF]\b'
    THEN   = r'[Tt][Hh][Ee][Nn]\b'
    ELSE =r'[Ee][Ll][Ss][Ee]\b'
    END    = r'[Ee][Nn][Dd]\b'
    BREAK  = r'[Bb][Rr][Ee][Aa][Kk]\b'
    RETURN = r'[Rr][Ee][Tt][uU][rR][nN]\b'
    SKIP= r'[sS][Kk][iI][pP]\b'
    BEGIN    = r'[Bb][Ee][Gg][Ii][Nn]\b'
    AND    = r'[Aa][Nn][Dd]\b'
    OR    = r'[Oo][Rr]\b'
    FLOAT_T  = r'[Ff][Ll][Oo][Aa][Tt]\b'
    INT_T = r'[iI][Nn][tT]\b'
    NAME = r'[a-zA-Z_]+[0-9a-zA-Z_]*'

    def error(self, t):
            print(f"Line {self.lineno}. Caracter ilegal '{t.value[0]}'")
            self.index += 1

    def __init__(self, context = None):
        self.context = context



def pprint(source):
    from rich.table   import Table
    from rich.console import Console


    lex = Lexer()
    print(" \n Comentarios : \n")


    table = Table(title='Analizador Léxico')
    table.add_column('token')
    table.add_column('value')
    table.add_column('lineno', justify='right')


    for tok in lex.tokenize(source):
        value = tok.value if isinstance(tok.value, str) else str(tok.value)
        table.add_row(tok.type, value, str(tok.lineno))

    console = Console()
    for comentario in Comentarios:
            print(comentario)

    print("\n")
    console.print(table, justify='center')




if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
       sys.stderr.write(f"usage: python {sys.argv[0]} fname")
       raise SystemExit(1)

    pprint(open(sys.argv[1], encoding='utf-8').read())