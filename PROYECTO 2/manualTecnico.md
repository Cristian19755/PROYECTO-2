 # MANUAL TECNICO

## Requisitos del sistema

1. Procesador CORE i3 en adelante
2. 1GB de RAM
3. Espacio en disco duro
4. SO windows 10 

## Herramientas utilizadas 

Para la construccion de este programa se utilizaron las herramientas de lex y yacc para el lenguaje de python, estas herramientas son de codigo abierto y se pueden descargar desde la pagina oficial de PLY https://www.dabeaz.com/ply/. Esta herramienta se apoyo de la gramatica descrita en este documento para generar el archivo parsetab.py el cual esta escrito en lenguaje de python y utiliza la gramatica y los apuntadores descritos en el programa main.py para generar las funciones lexer y parser utilizadas posteriormente para el analisis de archivos. Ademas, se utilizo tkinter para la construccione de la interfaz grafica. Y tambien la herramienta de PrettyTable para tabular la tabla de simbolos.


## LISTA DE TOKENS RECONOCIDOS POR EL PROGRAMA

| Token                    | Patron                                                                 |
| ------------------------ | -----------------------------------------------------------            |
| comentario_monolinea     | //.+                                                                   |
| comentario_multilinea    | (\/\*(\s*|.*?)*\*\/)                                                   |
| tipo_double              | (d\|D)(o\|O)(u\|U)(b\|B)(l\|L)(e\|E)                                   |
| tipo_int                 | (i\|I)(n\|N)(t\|T)                                                     |
| tipo_boolean             | (b\|B)(o\|O)(o\|O)(l\|L)                                               |
| tipo_String              | (s\|S)(t\|T)(r\|R)(i\|I)(n\|N)(g\|G)                                   |
| tipo_char                | (c\|C)(h\|H)(a\|A)(r\|R)                                               |
| reservada_void           | (v\|V)(o\|O)(i\|I)(d\|D)                                               |
| dato_double              | -?[0-9]+[.][0-9]+                                                      |
| dato_int                 | -?[0-9]+                                                               |
| dato_char                | '[^\s^']'                                                              |
| dato_string              | "[^\n^"]+"                                                             |
| dato_boolean             | ([tT][rR][uU][eE])\|([fF][aA][lL][sS][eE])                             |
| operador_suma            | +                                                                      |
| operador_resta           | -                                                                      |
| operador_multiplicacion  | *                                                                      |
| operador_división        | /                                                                      |
| operador_modulo          | %                                                                      |
| operador_ternario        | ?                                                                      |
| operador_potencia        | ^                                                                      |
| cor_a                    | [                                                                      |
| corb                     | ]                                                                      |
| operador_igualación      | ==                                                                     |
| operador_asignacion      | =                                                                      |
| operador_diferenciación  | !=                                                                     |
| operador_mayor_igual     | >=                                                                     |
| operador_mayor           | >                                                                      |
| operador_menor_igual     | <=                                                                     |
| operador_menor           | <                                                                      |
| operador_and             | &&                                                                     |
| operador_or              | \|\|                                                                   |
| operador_not             | !                                                                      |
| punto_coma               | ;                                                                      |
| coma                     | ,                                                                      |
| reservada_if             | (i\|I)(f\|F)                                                           |
| reservada_else           | (e\|E)(l\|L)(s\|S)(e\|E)                                               |
| reservada_while          | (w\|W)(h\|H)(i\|I)(l\|L)(e\|E)                                         |
| reservada_do             | (d\|D)(o\|O)                                                           |
| reservada_return         | (r\|R)(e\|E)(t\|T)(u\|U)(r\|R)(n\|N)                                   |
| reservada_break          | (b\|B)(r\|R)(e\|E)(a\|A)(k\|K)                                         |
| reservada_continue       | (c\|C)(o\|O)(n\|N)(t\|T)(i\|I)(n\|N)(u\|U)(e\|E)                       |  
| par_a                    | (                                                                      |
| par_b                    | )                                                                      |
| llave_a                  | {                                                                      |
| llave_b                  | }                                                                      |
| reservada_switch         | (s|S)(w|W)(i|I)(t|T)(c|C)(h|h)                                         |
| reservada_case           | (c|C)(a|A)(s|S)(e|E)                                                   |
| reservada_default        | (d|D)(e|E)(f|F)(a|A)(u|U)(l|L)(t|T)                                    |
| reservada_writeln        | (w|W)(r|R)(i|I)(t|T)(e|E)(l|L)(i|I)(n|N)(e|E)                          |
| reservada_for            | (f|F)(o|O)(r|R)                                                        |
| reservada_for            | (n|N)(e|E)(w|W)                                                        |
| dos_puntos               | :                                                                      |


## PRECEDENCIA

  |ASOCIACIATIVIDAD|OPERADOR|
  |-----|------|
  |'left'|'or'|
  |'left'|'and'|
  |'right'|'not'|
  |'left'|'igualacion','negacion','menor_que', 'mayor_que', 'mayor_igual', 'menor_igual'|
  |'left'|'suma','resta'|
  |'left'|'multiplicacion','division','modulo'|
  |'nonassoc'|'potencia'|
  |'nonassoc'|'incremental','decremental'|    

## GRAMATICAS

### Simbolo inicial

    ini : PROGRAMA

    PROGRAMA : PROGRAMA INSTRUCCIONES
             | INSTRUCCIONES

### Controlador de instrucciones

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

### Imprimir en pantalla(WriteLine)

    PRINT : reservada_writeln par_A EXPRESION par_B punto_coma

### Comentarios

    COMENTARIO : COMENTARIO1
               | COMENTARIO2

    COMENTARIO1 : comentario_monolinea

    COMENTARIO2 : comentario_multilinea

### Estructura Condicional (If)

    IF : reservada_if par_a DATO par_b llave_a CB llave_b reservada_else llave_a CBE llave_b 
       | reservada_if par_a DATO par_b llave_a CB llave_b
       | reservada_if par_a DATO par_b llave_a CB llave_b reservada_else IF
    
    CB : CB BIF
       | BIF
    
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
    
    CBE : CBE BIF
       | BIF

### Estructura de Seleccion (Switch)
    
    SWITCH : reservada_switch par_a DATO par_b llave_a CASE reservada_default dpuntos CD llave_b

    CASE : CASE reservada_case DATO dpuntos CS 
         | reservada_case DATO dpuntos CS
    
    CS : CS BS
       | BS
    
    BS : COMENTARIO
        | ASIGNACION
        | VECTOR
        | ACCESO
        | PRINT
        | IF
        | SWITCH
        | reservada_break pcoma
        | ESTRUCTURAS_ITERATIVAS

    CD : CD BD
       | BD
    
    BD : COMENTARIO
        | ASIGNACION
        | VECTOR
        | ACCESO
        | PRINT
        | IF
        | SWITCH
        | reservada_break pcoma
        | ESTRUCTURAS_ITERATIVAS

### Estructuras Iterativas (while, do while y for)

    ESTRUCTURAS_ITERATIVAS : reservada_while par_a DATO par_b llave_a CB llave_b
                           | reservada_do llave_a CB llave_b reservada_while par_a DATO par_b pcoma
                           | reservada_for par_a TIPO DATO igual DATO pcoma DATO pcoma DATO par_b  llave_a CB llave_b
 
### Metodos y funciones  

    PARAMETRO : PARAMETRO coma TIPO identificador
              | TIPO identificador
    
    FUNCION : TIPO identificador par_a PARAMETRO par_b llave_a CB llave_b
            | TIPO identificador par_a par_b llave_a CB llave_b

### Declaracion y asignacion

    ASIGNACION : TIPO ASIGNACION igual DATO pcoma
               | ASIGNACION igual DATO pcoma
               | ASIGNACION coma identificador
               | TIPO ASIGNACION pcoma
               | identificador
    
    DATO : EXPRESION
         | BOOLEAN
         | dato_string
         | dato_char
         | TERNARIO
         | ACCESO
    
    TERNARIO : BOOLEAN ternario DATO dpuntos DATO 

    TIPO : tipo_int
         | tipo_char
         | tipo_double
         | tipo_boolean
         | tipo_string
         | reservada_void

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
    
    NUM : dato_int
        | dato_double
        | identificador
        | dato_string
        | dato_char

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