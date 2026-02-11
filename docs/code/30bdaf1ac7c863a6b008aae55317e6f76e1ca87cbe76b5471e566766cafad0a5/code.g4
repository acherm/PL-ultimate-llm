/*
 * Grammer for JSON
 * See http://www.json.org/
 * Based on http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf
 */
grammar JSON;

json
    :   value
    ;

obj
    :   '{' pair (',' pair)* '}'
    |   '{' '}'
    ;

pair
    :   STRING ':' value
    ;

arr
    :   '[' value (',' value)* ']'
    |   '[' ']'
    ;

value
    :   STRING
    |   NUMBER
    |   obj
    |   arr
    |   'true'
    |   'false'
    |   'null'
    ;

STRING
    :   '"' (ESC | ~["\\])* '"'
    ;

fragment ESC
    :   '\\' (["\\/bfnrt] | UNICODE)
    ;

fragment UNICODE
    :   'u' HEX HEX HEX HEX
    ;

fragment HEX
    :   [0-9a-fA-F]
    ;

NUMBER
    :   '-'? INT ('.' [0-9]+)? EXP?
    ;

fragment INT
    :   '0' | [1-9] [0-9]*
    ;

// no leading zeros

fragment EXP
    :   [Ee] [+\-]? INT
    ;

// caseless

WS
    :   [ \t\n\r]+ -> skip
    ;