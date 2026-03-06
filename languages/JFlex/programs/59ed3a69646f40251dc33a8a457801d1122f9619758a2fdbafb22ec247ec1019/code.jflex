/* JFlex example: simple word and line counter */

%%

%class WordCounter
%standalone

%{
  int lines = 0, words = 0, chars = 0;
%}

nl  = \r|\n|\r\n
word = [^ \t\r\n]+

%%

{nl}    { lines++; chars += yylength(); }
{word}  { words++; chars += yylength(); }
.       { chars++; }
<<EOF>> { System.out.println("Lines: "+lines+", Words: "+words+", Chars: "+chars); }
