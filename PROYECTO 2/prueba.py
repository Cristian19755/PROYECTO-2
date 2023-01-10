import prettytable as pt
from graphviz import Digraph as Dig
global z, y, NODOS2, NODOS3, CASES
z = Dig('AST', filename='AST',format='SVG')
y = 0
nodos = []
NODOS2 = []
NODOS3 = []
CASES = []

## TABLA DE SIMBOLOS
ID = []
TIPO1 = []
TIPO2 = []
ENTORNO = []
LINEA = []
COLUMNA = []

INTORNO = '--'
entorno = 0

def getColumn(t):
  line_start = INPUT.rfind('\n', 0, t.lexpos) + 1
  return (t.lexpos-line_start)+1

def patron(type):
    ## comentarios
    if type == 'comentario_monolinea':
        return r'//.+'
    elif type == 'comentario_multilinea':
        return r'(\/\*(\s*|.*?)*\*\/)'

    ## writeln
    elif type == 'reservada_writeln':
        return r'(w|W)(r|R)(i|I)(t|T)(e|E)(l|L)(i|I)(n|N)(e|E)'

    ## Tipos de datos
    if type == 'tipo_int':
        return r'(i|I)(n|N)(t|T)'
    elif type == 'tipo_double':
        return r'(d|D)(o|O)(u|U)(b|B)(l|L)(e|E)'
    elif type == 'tipo_string':
        return r'(s|S)(t|T)(r|R)(i|I)(n|N)(g|G)'
    elif type == 'tipo_char':
        return r'(c|C)(h|H)(a|A)(r|R)'
    elif type == 'tipo_boolean':
        return r'(b|B)(o|O)(o|O)(l|L)(e|E)(a|A)(n|N)'
    
    ## Datos

    elif type == 'dato_double':
        return r'-?[0-9]+[.][0-9]+'
    elif type == 'dato_int':
        return r'-?[0-9]+'
    elif type == 'dato_string':
        return r'"[^\n^"]+"'
    elif type == 'dato_char':
        return r'\'[^\s^\']\''
    elif type == 'reservada_true':
        return r'(T|t)(R|r)(U|u)(E|e)'
    elif type == 'reservada_false':
        return r'([fF][aA][lL][sS][eE])'
        
    ## New
    elif type == 'reservada_new':
        return r'(n|N)(e|E)(w|W)' 

    ## Operadores
    elif type == 'incremental':
        return r'\+\+' 
    elif type == 'decremental':
        return r'--' 
    elif type == 'suma':
        return r'\+' 
    elif type == 'resta':
        return r'-' 
    elif type == 'multiplicacion':
        return r'\*' 
    elif type == 'division':
        return r'/'
    elif type == 'potencia':
        return r'\^' 
    elif type == 'modulo':
        return r'%' 


    elif type == 'igualacion':
        return r'==' 
    elif type == 'negacion':
        return r'!=' 
    elif type == 'mayor_igual':
        return r'>=' 
    elif type == 'menor_igual':
        return r'<='

    elif type == 'igual':
        return r'='  
    elif type == 'not':
        return r'!' 
    elif type == 'menor_que':
        return r'<' 
    elif type == 'mayor_que':
        return r'>' 
    elif type == 'ternario':
        return r'\?'
    elif type == 'or':
        return r'\|\|'
    elif type == 'and':
        return r'&&'
    
    ## Encapsuladores
    elif type == 'cor_a':
        return r'\[' 
    elif type == 'cor_b':
        return r'\]' 
    elif type == 'llave_a':
        return r'{' 
    elif type == 'llave_b':
        return r'}' 
    elif type == 'par_a':
        return r'\(' 
    elif type == 'par_b':
        return r'\)'
    elif type == 'dpuntos':
        return r':' 
    elif type == 'coma':
        return r','
    elif type == 'pcoma':
        return r';' 

    ## IF

    elif type == 'reservada_if':
        return r'(I|i)(f|F)'
    elif type == 'reservada_else':
        return r'([eE][lL][sS][eE])'
    elif type == 'reservada_return':
        return r'([Rr][Ee][Tt][Uu][Rr][Nn])'
    elif type == 'reservada_continue':
        return r'([Cc][Oo][Nn][Tt][Ii][Nn][Uu][Ee])'

    ## Switch
    elif type == 'reservada_switch':
        return r'(s|S)(w|W)(i|I)(t|T)(c|C)(h|h)'
    elif type == 'reservada_case':
        return r'(c|C)(a|A)(s|S)(e|E)'
    elif type == 'reservada_default':
        return r'(d|D)(e|E)(f|F)(a|A)(u|U)(l|L)(t|T)'
    elif type == 'reservada_break':
        return r'(b|B)(r|R)(e|E)(a|A)(k|K)'
    
    ## SENTENCIAS CICLICAS
    elif type == 'reservada_for':
        return r'(f|F)(o|O)(r|R)'
    elif type == 'reservada_while':
        return r'(w|W)(h|H)(i|I)(l|L)(e|E)'
    elif type == 'reservada_do':
        return r'(d|D)(o|O)'

    ## FUNCION

    elif type == 'reservada_void':
        return r'(v|V)(o|O)(i|I)(d|D)'
    
    #id
    elif type == 'identificador':
        return r'[a-zA-Z_][a-zA-Z0-9_]*'

# Reservadas

reserved = {
  'INT': 'tipo_int',
  'DOUBLE': 'tipo_double',
  'STRING': 'tipo_string',
  'CHAR': 'tipo_char',
  'BOOL': 'tipo_boolean',
  'IF': 'reservada_if',
  'ELSE':'reservada_else',
  'WHILE':'reservada_while',
  'DO':'reservada_do',
  'RETURN':'reservada_return',
  'BREAK':'reservada_break',
  'CONTINUE':'reservada_continue',
  'VOID':'reservada_void',
  'SWITCH': 'reservada_switch',
  'CASE': 'reservada_case',
  'DEFAULT': 'reservada_default',
  'WRITELINE': 'reservada_writeln',
  'FOR': 'reservada_for',
  'NEW': 'reservada_new',
  'TRUE': 'reservada_true',
  'FALSE': 'reservada_false',
}

# Tokens

tokens = (
  'comentario_monolinea',
  'comentario_multilinea',
  'reservada_writeln',
  'tipo_int',
  'tipo_double',
  'tipo_char',
  'tipo_boolean',
  'tipo_string',
  'dato_int',
  'dato_double',
  'dato_string',
  'dato_char',
  'reservada_true',
  'reservada_false',
  'identificador',
  'reservada_new',
  'suma',
  'resta',
  'multiplicacion',
  'division',
  'potencia',
  'modulo',
  'incremental',
  'decremental',
  'igual',
  'mayor_que',
  'menor_que',
  'not',
  'igualacion',
  'negacion',
  'mayor_igual',
  'menor_igual',
  'ternario',
  'or',
  'and',
  'cor_a',
  'cor_b',
  'par_a',
  'par_b',
  'llave_a',
  'llave_b',
  'pcoma',
  'coma',
  'dpuntos',
  'reservada_if',
  'reservada_else',
  'reservada_return',
  'reservada_continue',
  'reservada_switch',
  'reservada_case',
  'reservada_default',
  'reservada_break',
  'reservada_do',
  'reservada_while',
  'reservada_for',
  'reservada_void',
)

## comentarios
t_comentario_monolinea = r'//.+'

## WriteLine
t_reservada_writeln = r'[wW][rR][iI][tT][eE][lL][iI][nN][eE]'

## Tipos de Datos
t_tipo_int = r'(i|I)(n|N)(t|T)'
t_tipo_double = r'(d|D)(o|O)(u|U)(b|B)(l|L)(e|E)'
t_tipo_char = r'(c|C)(h|H)(a|A)(r|R)'
t_tipo_boolean = r'(b|B)(o|O)(o|O)(l|L)(e|E)(a|A)(n|N)'
t_tipo_string = r'(s|S)(t|T)(r|R)(i|I)(n|N)(g|G)'

## Datos 
t_dato_int = r'-?[0-9]+'
t_dato_double =  r'-?[0-9]+[.][0-9]+'
t_dato_char = r'\'[^\s^\']\''
t_dato_string = r'"[^\n^"]+"'
t_reservada_true = r'(t|T)(r|R)(u|U)(e|E)'
t_reservada_false = r'(f|F)(a|A)(l|L)(s|S)(e|E)'

## New
t_reservada_new = r'(n|N)(e|E)(w|W)'

## Operadores

t_suma = r'\+'
t_resta = r'-'
t_multiplicacion = r'\*'
t_division = r'/'
t_potencia = r'\^'
t_incremental = r'\+\+'
t_decremental = r'--'
t_modulo = r'%'
t_igual = r'='
t_igualacion = r'=='
t_not = r'!'
t_negacion = r'!='
t_menor_que = r'<'
t_mayor_que = r'>'
t_menor_igual = r'<='
t_mayor_igual = r'>='
t_ternario = r'\?'
t_and = r'&&'
t_or = r'\|\|'

## Encapsuladores
t_cor_a = r'\['
t_cor_b = r'\]'
t_par_a = r'\('
t_par_b = r'\)'
t_llave_a = r'{'
t_llave_b = r'}'
t_pcoma = r';'
t_coma = r','
t_dpuntos = r':'

## IF
t_reservada_if = r'(I|i)(f|F)'
t_reservada_else = r'(e|E)(l|L)(s|S)(e|E)'
t_reservada_return = r'(r|R)(e|E)(t|T)(u|U)(r|R)(n|N)'
t_reservada_continue = r'(c|C)(o|O)(n|N)(t|T)(i|I)(n|N)(u|U)(e|E)'

## Switch

t_reservada_switch = r'(s|S)(w|W)(i|I)(t|T)(c|C)(h|H)'
t_reservada_case = r'(c|C)(a|A)(s|S)(e|E)'
t_reservada_default = r'(d|D)(e|E)(f|F)(a|A)(u|U)(l|L)(t|T)'
t_reservada_break = r'(b|B)(r|R)(e|E)(a|A)(k|K)'

## SENTENCIAS CICLICAS
t_reservada_for = r'(f|F)(o|O)(r|R)'
t_reservada_while = r'(w|W)(h|H)(i|I)(l|L)(e|E)'
t_reservada_do = r'(d|D)(o|O)'

## FUNCION
t_reservada_void = r'(v|V)(o|O)(i|I)(d|D)'

def t_identificador(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  if t.value.upper() in reserved.keys(): t.type = reserved[t.value.upper()]
  return t

def t_comentario_multilinea(t):
  r'(\/\*(\s*|.*?)*\*\/)'
  for i in t.value:
    if i == '\n':
        t.lexer.lineno+=1
  return t


# Lexemas ignorados
t_ignore = ' \t\r'

def t_newline(t):
  r'\n+'
  t.lexer.lineno+=len(t.value)

def t_error(t): 
    x = '''<tr>
                <td style="text-align: center;">'''+ str(t.lineno) +'''</td>
                <td style="text-align: center;">'''+ str(getColumn(t)) +'''</td>
                <td style="text-align: center;">'''+ 'LEXICO' +'''</td>
                <td style="text-align: center;">'''+ 'No se reconoce el lexema '+str(t.value[0]) +'''</td>
                </tr>''' 
    t.lexer.skip(1)
    file = open('errores.txt','a')
    file.write(x)
    file.close()

## Precedencia
precedence = (
  ('left','or'),
  ('left','and'),
  ('right','not'),
  ('left','igualacion','negacion','menor_que', 'mayor_que', 'mayor_igual', 'menor_igual'),
  ('left','suma','resta'),
  ('left','multiplicacion','division','modulo'),
  ('nonassoc','potencia'),
  ('nonassoc','incremental','decremental'),
)

# Producciones
### RAIZ

def p_ini(p):
    '''
    ini : PROGRAMA
    '''
    z.view()
    x = pt.PrettyTable()
    x.field_names=['ID','TIPO1','TIPO2','ENTORNO','LINEA','COLUMNA']
    for i in range(len(ID)):
        x.add_row([ID[i],TIPO1[i],TIPO2[i],ENTORNO[i],LINEA[i],COLUMNA[i]])
    print(x)

### ITERADOR PRINCIPAL 

def p_PROGRAMA(p):
    '''
    PROGRAMA : PROGRAMA INSTRUCCIONES
             | INSTRUCCIONES
    '''
    if len(p) == 3: 
        z.edge('INICIO', p[2])
        p[0]='INICIO'
    else:
        z.node('INICIO','INICIO', style='filled', fillcolor='red:ORANGE', fontcolor='WHITE',gradientangle='45')
        z.edge('INICIO', p[1])
        p[0]='INICIO'
        
### CONTROLADOR DE DIRECCION

def p_INSTRUCCIONES(p):
    '''
    INSTRUCCIONES : COMENTARIO
                  | ASIGNACION
                  | VECTOR
                  | ACCESO
                  | PRINT
                  | IF
                  | SWITCH
                  | ESTRUCTURAS_ITERATIVAS
                  | DATO pcoma
                  | FUNCION
    '''
    p[0] = p[1]

## Funcion

def p_FUNCION(p):
    '''
    FUNCION : TIPO identificador par_a PARAMETRO par_b llave_a CB llave_b
            | TIPO identificador par_a par_b llave_a CB llave_b
    '''
    global y, ENTORNO, entorno, ID, TIPO1, TIPO2, LINEA, COLUMNA, INTORNO
    INTORNO = p[2]
    if len(p) == 9:
        
        x = 'NODE'+str(y)
        z.node(x, str(p[4]))
        y += 1

        V = 'NODE'+str(y)
        z.node(V, 'FUNCION',  style='filled', fillcolor='GREEN', fontcolor='WHITE')
        z.edge(V, x)
        y += 1

        B = 'NODE'+str(y)
        z.node(B, 'FUNSTRUCCIONES')
        z.edge(V, B)
        y += 1

        W = 'NODE'+str(y)
        z.node(W, str(p[1]))
        y += 1

        C = 'NODE'+str(y)
        z.node(C, str(p[2]))
        y += 1

        z.edge(V, W)
        z.edge(V, C)

        for i in NODOS2:
            if p[7] != 0:
                z.edge(B,i)
                p[7]-=1

        p[0] = V

        ID.append(str(p[2]))
        ENTORNO.append('--')
        TIPO1.append(str(p[1]))
        TIPO2.append('FUNCION')
        LINEA.append(p.lineno(2))
        line_start = INPUT.rfind('\n', 0, p.lexpos(2)) + 1
        COLUMNA.append((p.lexpos(2)-line_start)+1)

    else:
        V = 'NODE'+str(y)
        z.node(V, 'FUNCION',  style='filled', fillcolor='GREEN', fontcolor='WHITE')
        y += 1

        B = 'NODE'+str(y)
        z.node(B, 'FUNSTRUCCIONES')
        z.edge(V, B)
        y += 1

        W = 'NODE'+str(y)
        z.node(W, str(p[1]))
        y += 1

        C = 'NODE'+str(y)
        z.node(C, str(p[2]))
        y += 1

        z.edge(V, W)
        z.edge(V, C)

        for i in NODOS2:
            if p[6] != 0:
                z.edge(B,i)
                p[6]-=1

        p[0] = V
        ID.append(str(p[2]))
        ENTORNO.append('--')
        TIPO1.append(str(p[1]))
        TIPO2.append('FUNCION')
        LINEA.append(p.lineno(2))
        line_start = INPUT.rfind('\n', 0, p.lexpos(2)) + 1
        COLUMNA.append((p.lexpos(2)-line_start)+1)
    INTORNO = '--'

def p_PARAMETRO(p):
    '''
    PARAMETRO : PARAMETRO coma TIPO identificador
              | TIPO identificador
    '''
    if len(p) == 5:
        p[0] = str(p[1]) + ', ' + str(p[3])+' '+ str(p[4]) 
    else:
        p[0] = str(p[2])+' '+str(p[2])

def p_ESTRUCTURAS_ITERATIVAS(p):
    '''
    ESTRUCTURAS_ITERATIVAS : reservada_while par_a DATO par_b llave_a CB llave_b
                           | reservada_do llave_a CB llave_b reservada_while par_a DATO par_b pcoma
                           | reservada_for par_a TIPO DATO igual DATO pcoma DATO pcoma DATO par_b  llave_a CB llave_b
    '''

    global y, NODOS2, NODOS3, ENTORNO, entorno, ID, TIPO1, TIPO2, LINEA, COLUMNA, INTORNO
    INTORNO = p[1]+str(entorno)
    entorno +=1
    if len(p) == 8:
        V = 'NODE'+str(y)
        z.node(V,'WHILE', style='filled', fillcolor='BLUE', fontcolor='WHITE')
        y += 1

        C = 'NODE'+str(y)
        z.node(C,'WHILESTRUCCIONES')
        y += 1

        X = p[3]
        for i in range(len(NODOS2)):
            if p[6] != 0:
                z.edge(C,NODOS2[len(NODOS2)-(i+1)])
                p[6]-=1
        z.edge(X,C)
        z.edge(V,X)
        p[0]=V

    elif len(p) == 10:
        V = 'NODE'+str(y)
        z.node(V,'DO_WHILE', style='filled', fillcolor='BLUE', fontcolor='WHITE')
        y += 1

        C = 'NODE'+str(y)
        z.node(C,'DOWHILESTRUCCIONES')
        y += 1

        X = p[7]
        for i in range(len(NODOS2)):
            if p[3] != 0:
                z.edge(C,NODOS2[len(NODOS2)-(i+1)])
                p[3]-=1
        z.edge(X,C)
        z.edge(V,X)
        p[0]=V
    else:
        V = 'NODE'+str(y)
        z.node(V,'FOR', style='filled', fillcolor='BLUE', fontcolor='WHITE')
        y += 1

        C = 'NODE'+str(y)
        z.node(C,'FORSTRUCCIONES')
        y += 1

        X = p[4]

        J = p[6]

        K = p[10]

        for i in range(len(NODOS2)):
            if p[13] != 0:
                z.edge(C,NODOS2[len(NODOS2)-(i+1)])
                p[13]-=1
        z.edge(V,C)
        z.edge(V,X)
        z.edge(V,J)
        z.edge(V,K)
        p[0]=V
    INTORNO = '--'

### SWITCH

def p_SWITCH(p):
    '''
    SWITCH : reservada_switch par_a DATO par_b llave_a CASE reservada_default dpuntos CD llave_b
    '''
    global NODOS2, CASES, y, NODOS3, ENTORNO, entorno, ID, TIPO1, TIPO2, LINEA, COLUMNA, INTORNO
    INTORNO = p[1]+str(entorno)
    entorno += 1
    V = 'NODE'+str(y)
    z.node(V,'SWITCH')
    y += 1   

    J = 'NODE'+str(y)
    z.node(J,'DEFAULT')
    y += 1   

    z.edge(V, J)
    z.edge(V,p[3])

    for i in range(len(CASES)):
        if p[6] != 0:
            z.edge(V,CASES[len(CASES)-(i+1)])
            p[6]-=1

    for i in range(len(NODOS3)):
        if p[9] != 0:
            z.edge(J,NODOS3[len(NODOS3)-(i+1)])
            p[9]-=1
    p[0] = V 
    CASES = []
    NODOS2 = []
    NODOS3 = []

    INTORNO = '--'

def p_CASE(p):
    '''
    CASE : CASE reservada_case DATO dpuntos CS 
         | reservada_case DATO dpuntos CS
    '''
    global y, NODOS2, CASES

    if len(p) == 5: 
        V = 'NODE'+str(y)
        V = p[2]
        y += 1   
        for i in range(len(NODOS2)):
            if p[4] != 0:
                z.edge(V,NODOS2[len(NODOS2)-(i+1)])
                p[4]-=1
        CASES.append(V)
        p[0] = 1 

    elif len(p)==6:
        V = 'NODE'+str(y)
        V=p[3]
        y += 1   
        for i in range(len(NODOS2)):
            if p[5] != 0:
                z.edge(V,NODOS2[len(NODOS2)-(i+1)])
                p[5]-=1
        CASES.append(V) 
        p[0] = 1 + p[1]

def p_CS(p):
    '''
    CS : CS BS
       | BS
    '''
    global y, NODOS2
    if len(p) == 3: 
        NODOS2.append(p[2]) 
        p[0] = p[1] + 1    
    elif len(p)==2:
        NODOS2.append(p[1])
        p[0] = 1

def p_BS(p):
    '''
    BS : COMENTARIO
        | ASIGNACION
        | VECTOR
        | ACCESO
        | PRINT
        | IF
        | SWITCH
        | reservada_break pcoma
        | ESTRUCTURAS_ITERATIVAS
    '''
    global y

    if len(p)==2:
        p[0]= p[1]
    elif len(p)==3:
        V = 'NODE'+str(y)
        z.node(V,p[1])
        y += 1
        p[0]=V

def p_CD(p):
    '''
    CD : CD BD
       | BD
    '''
    global y, NODOS3
    if len(p) == 3: 
        NODOS3.append(p[2]) 
        p[0] = p[1] + 1    
    elif len(p)==2:
        NODOS3.append(p[1])
        p[0] = 1

def p_BD(p):
    '''
    BD : COMENTARIO
        | ASIGNACION
        | VECTOR
        | ACCESO
        | PRINT
        | IF
        | SWITCH
        | reservada_break pcoma
        | ESTRUCTURAS_ITERATIVAS
    '''
    global y
    if len(p)==2:
        p[0]= p[1]
    elif len(p)==3:
        V = 'NODE'+str(y)
        z.node(V,p[1])
        y += 1
        p[0]=V

## IF
def p_IF(p):
    '''
    IF : reservada_if par_a DATO par_b llave_a CB llave_b reservada_else llave_a CBE llave_b 
       | reservada_if par_a DATO par_b llave_a CB llave_b
       | reservada_if par_a DATO par_b llave_a CB llave_b reservada_else IF
    '''

    global y, NODOS2, NODOS3, ENTORNO, entorno, ID, TIPO1, TIPO2, LINEA, COLUMNA, INTORNO
    INTORNO = p[1]+str(entorno)
    entorno += 1
    if len(p)==12:
        V = 'NODE'+str(y)
        z.node(V,'IF', style='filled', fillcolor='red', fontcolor='WHITE')
        y += 1        

        W = 'NODE'+str(y)
        z.node(W,'ELSE')
        y += 1

        C = 'NODE'+str(y)
        z.node(C,'IFSTRUCCIONES')
        y += 1

        B = 'NODE'+str(y)
        z.node(B,'ELSTRUCCIONES')
        y += 1

        z.edge(W,B)
        
        X = p[3]

        z.edge(X,C)

        for i in NODOS2:
            if p[6] != 0:
                z.edge(C,i)
                p[6]-=1

        for j in NODOS3:
            z.edge(B,j)
        NODOS3=[]


        z.edge(V,X)
        z.edge(V,W)
        p[0]=V

    elif len(p)==8:
        V = 'NODE'+str(y)
        z.node(V,'IF', style='filled', fillcolor='red', fontcolor='WHITE')
        y += 1

        C = 'NODE'+str(y)
        z.node(C,'IFSTRUCCIONES',)
        y += 1

        X = p[3]
        for i in range(len(NODOS2)):
            if p[6] != 0:
                z.edge(C,NODOS2[len(NODOS2)-(i+1)])
                p[6]-=1
        z.edge(X,C)
        z.edge(V,X)
        p[0]=V

    elif len(p)==10:
        V = 'NODE'+str(y)
        z.node(V,'IF', style='filled', fillcolor='red', fontcolor='WHITE')
        y += 1        

        W = 'NODE'+str(y)
        z.node(W,'ELSE')
        y += 1

        C = 'NODE'+str(y)
        z.node(C,'IFSTRUCCIONES')
        y += 1

        for i in NODOS2:
            if p[6] != 0:
                z.edge(C,i)
                p[6]-=1

        B = 'NODE'+str(y)
        z.node(B,'ELSTRUCCIONES')
        y += 1

        z.edge(W,B)
        
        X = p[3]

        z.edge(X,C)
        
        z.edge(B,p[9])

        z.edge(V,X)
        z.edge(V,W)
        p[0]=V
        NODOS2 = []
    INTORNO = '--'

def p_CB(p):
    '''
    CB : CB BIF
       | BIF
    '''
    global y, NODOS2

    if len(p) == 3: 
        NODOS2.append(p[2]) 
        p[0] = p[1] + 1    
    elif len(p)==2:
        NODOS2.append(p[1])
        p[0] = 1

def p_BIF(p):
    '''
    BIF : COMENTARIO
        | ASIGNACION
        | VECTOR
        | ACCESO
        | PRINT
        | IF
        | SWITCH
        | reservada_return pcoma
        | reservada_return DATO pcoma
        | reservada_continue pcoma
        | reservada_break pcoma
        | ESTRUCTURAS_ITERATIVAS
        
    '''
    global y
    if len(p)==2:
        p[0]= p[1]
    elif len(p)==3:
        V = 'NODE'+str(y)
        z.node(V,p[1])
        y += 1
        p[0]=V
    elif len(p)==4:
        V = 'NODE'+str(y)
        z.node(V,'return')
        y += 1
        z.edge(V,p[2])
        p[0]=V
    
def p_CBE(p):
    '''
    CBE : CBE BIF
       | BIF
    '''
    global y, NODOS3

    if len(p) == 3: 
        NODOS3.append(p[2])      
    elif len(p)==2:
        NODOS3.append(p[1])
        
### WRITELINE
def p_PRINT(p):
    '''
    PRINT : reservada_writeln par_a DATO par_b pcoma
    '''
    
    global y
    x =p[3]
    V = 'NODE'+str(y)
    z.node(V, 'WRITELINE')
    z.edge(V, x)
    y += 1
    p[0] = V

### COMENTARIOS 
def p_COMENTARIO(p):
    '''
    COMENTARIO : COMENTARIO1
               | COMENTARIO2
    '''
    global y
    x = 'NODE'+str(y)
    z.node(x, str(p[1]))
    y += 1
    V = 'NODE'+str(y)
    z.node(V, 'COMENTARIO')
    z.edge(V, x)
    y += 1

    p[0] = V
    
def p_COMENTARIO1(p):
    '''
    COMENTARIO1 : comentario_monolinea
    '''
    p[0] = str(p[1])

def p_COMENTARIO2(p):
    '''
    COMENTARIO2 : comentario_multilinea
    '''
    p[0] = str(p[1])

## VECTOR 
def p_VECTOR(p):
    '''
    VECTOR : TIPO identificador cor_a cor_b igual reservada_new TIPO cor_a EXPRESION cor_b pcoma 
           | TIPO identificador cor_a cor_b igual llave_a VECTOR llave_b pcoma 
           | VECTOR coma DATO 
           | DATO 
    '''

    global y, NODOS2, ENTORNO, entorno, ID, TIPO1, TIPO2, LINEA, COLUMNA, INTORNO
    
    if len(p)==12:
        w = 'NODE'+str(y)
        z.node(w, p[2])
        y += 1
        
        x = 'NODE'+str(y)
        z.node(x, '[ ]')
        y += 1

        c = p[9]

        z.edge(x,c)

        V = 'NODE'+str(y)
        z.node(V, 'VECTOR '+p[1])
        z.edge(V, x)
        z.edge(V, w)
        y += 1

        G = 'NODE'+str(y)
        z.node(G, 'DECLARACION')
        z.edge(G, V)
        y += 1
        p[0] = G

        ID.append(str(p[2]))
        ENTORNO.append(INTORNO)
        TIPO1.append(str(p[1]))
        TIPO2.append('VECTOR')
        LINEA.append(p.lineno(2))
        line_start = INPUT.rfind('\n', 0, p.lexpos(2)) + 1
        COLUMNA.append((p.lexpos(2)-line_start)+1)

    elif len(p)==10:
        w = 'NODE'+str(y)
        z.node(w, p[2])
        y += 1

        c = 'NODE'+str(y)
        z.node(c, '[ ]')
        y += 1


        for i in NODOS2:
            z.edge(c,i)
        NODOS2= []
        V = 'NODE'+str(y)
        z.node(V, 'VECTOR '+p[1])
        z.edge(V, c)
        z.edge(V, w)
        y += 1

        G = 'NODE'+str(y)
        z.node(G, 'ASIGNACION')
        z.edge(G, V)
        y += 1
        p[0] = G

        ID.append(str(p[2]))
        ENTORNO.append(INTORNO)
        TIPO1.append(str(p[1]))
        TIPO2.append('VECTOR')
        LINEA.append(p.lineno(2))
        line_start = INPUT.rfind('\n', 0, p.lexpos(2)) + 1
        COLUMNA.append((p.lexpos(2)-line_start)+1)

    elif len(p)==4:
        p[0] = NODOS2.append(p[3]) 
    elif len(p)==2:
        p[0] = NODOS2.append(p[1])

def p_ACCESO(p):
    '''
    ACCESO : identificador cor_a EXPRESION cor_b
           | identificador cor_a EXPRESION cor_b igual DATO pcoma
    '''
    global y
    if len(p)==5:
        w = 'NODE'+str(y)
        z.node(w, p[1])
        y += 1 
        if p[3] in nodos:
            x = p[3] 
        else:
            x = 'NODE'+str(y)
            z.node(x, 'pos: '+str(p[3]))
            y += 1
        z.edge(w,x)
        nodos.append(w)
        p[0]=w

    elif len(p) == 8:
        w = 'NODE'+str(y)
        z.node(w, p[1])
        y += 1 
        if p[3] in nodos:
            x = p[3] 
        else:
            x = 'NODE'+str(y)
            z.node(x, 'pos: '+str(p[3]))
            y += 1

        if p[6] in nodos:
            c = p[6] 
        else:
            c = 'NODE'+str(y)
            z.node(c, str(p[6]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, 'MODIFICAR')
        y += 1 
        z.edge(V,w)
        z.edge(V,x)
        z.edge(V,c)
        p[0]=V
    
## ASIGNACION Y DECLARACION
def p_ASIGNACION(p):
    '''
    ASIGNACION : TIPO ASIGNACION igual DATO pcoma
               | ASIGNACION igual DATO pcoma
               | ASIGNACION coma identificador
               | TIPO ASIGNACION pcoma
               | identificador
    '''
    global y, ENTORNO, ID, TIPO1, TIPO2, LINEA, COLUMNA, INTORNO
    if len(p) ==6:
        w = 'NODE'+str(y)
        z.node(w, p[2])
        y += 1
 
        c = p[4]

        V = 'NODE'+str(y)
        z.node(V, p[1])
        z.edge(V, c)
        z.edge(V, w)
        y += 1

        G = 'NODE'+str(y)
        z.node(G, 'ASIGNACION')
        z.edge(G, V)
        y += 1
        p[0] = G

        ID.append(str(p[2]))
        ENTORNO.append(INTORNO)
        TIPO1.append(str(p[1]))
        TIPO2.append('VARIABLE')
        LINEA.append(p.lineno(2))
        line_start = INPUT.rfind('\n', 0, p.lexpos(2)) + 1
        COLUMNA.append((p.lexpos(2)-line_start)+1)

    elif len(p) == 5:
        w = 'NODE'+str(y)
        z.node(w, p[1])
        y += 1

        c = p[3]

        V = 'NODE'+str(y)
        z.node(V, 'ASIGNACION')
        z.edge(V, c)
        z.edge(V, w)
        y += 1

        G = 'NODE'+str(y)
        y += 1
        p[0] = V
        ID.append(str(p[1]))
        ENTORNO.append(INTORNO)
        TIPO1.append('NONE')
        TIPO2.append('VARIABLE')
        LINEA.append(p.lineno(2))
        line_start = INPUT.rfind('\n', 0, p.lexpos(2)) + 1
        COLUMNA.append((p.lexpos(2)-line_start)+1)

    elif len(p)==4:
        if p[2] ==',':
            p[0]=str(p[1])+', '+str(p[3])
        else:
            w = 'NODE'+str(y)
            z.node(w, p[1])
            y += 1
            c = p[2]
            V = 'NODE'+str(y)
            z.node(V, 'DECLARACION')
            z.edge(V, c)
            z.edge(V, w)
            y += 1
            p[0] = V
            ID.append(str(p[2]))
            ENTORNO.append(INTORNO)
            TIPO1.append(str(p[1]))
            TIPO2.append('VARIABLE')
            LINEA.append(p.lineno(2))
            line_start = INPUT.rfind('\n', 0, p.lexpos(2)) + 1
            COLUMNA.append((p.lexpos(2)-line_start)+1)
    elif len(p)==2:
        p[0]=str(p[1])

## DATO
def p_DATO(p):
    '''
    DATO : EXPRESION
         | BOOLEAN
         | dato_string
         | dato_char
         | TERNARIO
         | ACCESO
    '''

    global y
    if p[1] in nodos:
        x = p[1] 
    else:
        x = 'NODE'+str(y)
        z.node(x, str(p[1]))
        y += 1
        nodos.append(x)
    p[0] = x
    
## TERNARIO
def p_TERNARIO(p):
    '''
    TERNARIO : BOOLEAN ternario DATO dpuntos DATO 
    '''
    global y
    if p[1] in nodos:
        x = p[1] 
    else:
        x = 'NODE'+str(y)
        z.node(x, str(p[1]))
        y += 1

    if p[3] in nodos:
        w = p[3] 
    else:
        w = 'NODE'+str(y)
        z.node(w, str(p[3]))
        y += 1

    if p[5] in nodos:
        c = p[5] 
    else:
        c = 'NODE'+str(y)
        z.node(c, str(p[5]))
        y += 1

    V = 'NODE'+str(y)
    z.node(V, '?')
    z.edge(V,x)
    z.edge(V,w)
    z.edge(V,c)
    y += 1
    p[0] = V
    nodos.append(V)

## TIPO
def p_TIPO(p):
    '''
    TIPO : tipo_int
         | tipo_char
         | tipo_double
         | tipo_boolean
         | tipo_string
         | reservada_void
    '''
    p[0] = str(p[1])

## Operacion Matematica

def p_EXPRESION(p):
    ''' 
    EXPRESION : EXPRESION suma EXPRESION
        | EXPRESION resta EXPRESION
        | EXPRESION multiplicacion EXPRESION
        | EXPRESION division EXPRESION
        | EXPRESION potencia EXPRESION
        | EXPRESION modulo EXPRESION
        | EXPRESION incremental
        | EXPRESION decremental
        | par_a EXPRESION par_b
        | NUM
    '''
    global y
    if len(p) == 4 and p[2] == '+'  : 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1

        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '+')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '-': 
        
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1

        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '-')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)
    elif len(p) == 4 and p[2] == '*': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1

        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '*')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)
    elif len(p) == 4 and p[2] == '/': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1

        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '/')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '^': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1

        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '^')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '%': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1

        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '%')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[1] == '(': 
        if p[2] in nodos:
            x = p[2] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[2]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '( )')
        z.edge(V, x)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 3 and p[2] == '++': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '++')
        z.edge(V, x)
        y += 1
        p[0] = V
        nodos.append(V)    
    
    elif len(p) == 3 and p[2] == '--': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '--')
        z.edge(V, x)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p)==2  : 
        p[0] = str(p[1])

def p_NUM(p):
    ''' 
    NUM : dato_int
        | dato_double
        | identificador
        | dato_string
        | dato_char
    '''    
    p[0] = str(p[1])

def p_BOOLEAN(p):
    ''' 
    BOOLEAN : BOOLEAN or BOOLEAN
            | BOOLEAN and BOOLEAN
            | BOOLEAN mayor_igual BOOLEAN
            | BOOLEAN mayor_que BOOLEAN
            | BOOLEAN menor_igual BOOLEAN
            | BOOLEAN menor_que BOOLEAN
            | BOOLEAN igualacion BOOLEAN
            | BOOLEAN negacion BOOLEAN
            | not BOOLEAN
            | par_a BOOLEAN par_b
            | reservada_false
            | reservada_true
            | identificador
            | EXPRESION
            | dato_string
            | dato_char
    '''
    global y
    if len(p) == 4 and p[2] == '||'  : 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1
        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '||')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '&&': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1

        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '&&')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '>': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1
        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '>')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '>=': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1

        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '>=')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '<': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1
        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '<')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '<=': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1
        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '<=')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 3 and p[1] == '!': 
        if p[2] in nodos:
            x = p[2] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[2]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '!')
        z.edge(V, x)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '!=': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1
        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '!=')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[2] == '==': 
        if p[1] in nodos:
            x = p[1] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[1]))
            y += 1
        if p[3] in nodos:
            w = p[3] 
        else:
            w = 'NODE'+str(y)
            z.node(w, str(p[3]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '==')
        z.edge(V, x)
        z.edge(V,w)
        y += 1
        p[0] = V
        nodos.append(V)

    elif len(p) == 4 and p[1] == '(': 
        if p[2] in nodos:
            x = p[2] 
        else:
            x = 'NODE'+str(y)
            z.node(x, str(p[2]))
            y += 1
        V = 'NODE'+str(y)
        z.node(V, '( )')
        z.edge(V, x)
        y += 1
        p[0] = V
        nodos.append(V)
    elif len(p)==2: 
        p[0] = p[1]

## Error sintactico
def p_error(p):
    if p:
        x = '''<tr>
                <td style="text-align: center;">'''+ str(p.lexer.lineno) +'''</td>
                <td style="text-align: center;">'''+ str(getColumn(p.lexer)) +'''</td>
                <td style="text-align: center;">'''+ 'SINTACTICO' +'''</td>
                <td style="text-align: center;">'''+ 'No se esperaba el lexema '+str(p.value) +'''</td>
                </tr>''' 
        file = open('errores.txt','a')
        file.write(x)
        file.close()
    else:
        print("EOF")


from ply.yacc import yacc
from ply.lex import lex
from tkinter import RAISED,Button, Entry, Label,Text, Tk, filedialog,END,INSERT

root = Tk()

root.geometry('1000x500')
global path, INPUT
path = ''
INPUT = ''

def analizar():
        global path, INPUT, C, nombre, root2
        nombre =''
        root2 = Tk()
        B = Label(root2,text='Nombre de los reportes: ')
        B.grid(row=1)
        C = Entry(root2)
        C.grid(row=2)
        D = Button(root2, text='Ok', command=ok)
        D.grid(row=3)

def cargar():
    global path, INPUT 
    INPUT = ''
    path = filedialog.askopenfilename()
    file = open(path,'r',encoding='utf-8')
    INPUT = file.read()
    F.insert(END, INPUT)

def ok():
    global C, nombre, root2, F
    nombre = C.get()
    root2.destroy()
    lexer = lex()
    parser = yacc()
    ast = parser.parse(INPUT, lexer, tracking=True)
    lexer.input(INPUT)
    y=''
    for tok in lexer:
        columna = getColumn(tok)
        lexema = tok.value
        linea = tok.lineno
        token = tok.type
        lexmatch = patron(token)
        if token != 'error':
            y += '''<tr>
                        <td style="text-align: center;">'''+ str(linea) +'''</td>
                        <td style="text-align: center;">'''+ str(columna) +'''</td>
                        <td style="text-align: center;">'''+ str(lexema) +'''</td>
                        <td style="text-align: center;">'''+ str(token) +'''</td>
                        <td style="text-align: center;">'''+ str(lexmatch) +'''</td>
                        </tr>''' 
    TOKENS = '''<table>
        <tbody>
        <tr style="background-color: #61FF57;">
        <td style="text-align: center;">LINEA</td>
        <td style="text-align: center;">COLUMNA</td>
        <td style="text-align: center;">LEXEMA</td>
        <td style="text-align: center;">TOKEN</td>
        <td style="text-align: center;">PATRON</td>
        </tr>''' + y + '''</tbody>
                    </table>'''
    text = '''<h1>ANALISIS LEXICO</h1><h1></h1>'''+TOKENS
    file = open(nombre+'-tokens.html','w')
    file.write(text)
    txt = open('errores.txt', 'r')
    errortxt = '''<h1>\nREPORTE DE ERRORES</h1><table>
        <tbody>
        <tr style="background-color: #61FF57;">
        <td style="text-align: center;">LINEA</td>
        <td style="text-align: center;">COLUMNA</td>
        <td style="text-align: center;">TIPO</td>
        <td style="text-align: center;">DESCRIPCION</td>
        '''+txt.read()+'''</tr><tr>'''
    txt.close()
    errorfile = open(nombre+'-errores.html','w')
    errorfile.write(errortxt)
    txt = open('errores.txt', 'w')
    txt.write('')
    txt.close()
    errorfile.close()

def salir():
    exit()

A = Button(root, text ='Cargar', command= cargar,  bg='red', fg='white',height=3, width=15)
A.grid(ipady=1, ipadx=0)
E = Button(root, text ='Analizar', command= analizar,  bg='blue', fg='white',height=3, width=15)
E.grid(ipady=2, ipadx=0)
E = Button(root, text ='Salir', command= salir,  bg='green', fg='white',height=3, width=15)
E.grid(ipady=3,ipadx=0)
F = Text(root, bg='yellow', width=105,fg='red')
F.insert(INSERT, INPUT)
F.grid(row=0,column=4)

root.mainloop()