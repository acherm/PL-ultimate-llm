%{
#include <stdio.h>
%}

%%
[0-9]+          { printf("NUMBER: %s\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]*  { printf("IDENTIFIER: %s\n", yytext); }
[ \t\n]        { /* skip whitespace */ }
.               { printf("UNKNOWN: %s\n", yytext); }
%%

int main(int argc, char **argv) {
    yylex();
    return 0;
}

int yywrap(void) {
    return 1;
}
