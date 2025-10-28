%%

cat|dog { printf( "animal\n" ); }

[ \t\n] ; /* white space */

. { printf( "NYI\n" ); }

%%

main()
{
    yylex();
    return 0;
}