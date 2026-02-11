%token NUMBER
%left '+' '-'
%left '*' '/'
%nonassoc UMINUS
%%
lines : lines expr '\n' { printf("%g\n", $2); }
 | lines '\n'
 | /* empty */
 | error '\n' { yyerrok; }
 ;
expr : expr '+' expr { $$ = $1 + $3; }
 | expr '-' expr { $$ = $1 - $3; }
 | expr '*' expr { $$ = $1 * $3; }
 | expr '/' expr { $$ = $1 / $3; }
 | '-' expr %prec UMINUS { $$ = -$2; }
 | '(' expr ')' { $$ = $2; }
 | NUMBER { $$ = $1; }
 ;
%%