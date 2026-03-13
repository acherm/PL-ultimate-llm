\ StrongForth: Factorial
\ Demonstrates statically-checked stack effects

: factorial  ( n -- n )
  dup 1 > if
    dup 1 - recurse *
  else
    drop 1
  then ;

: main  ( -- )
  5 factorial . cr
  10 factorial . cr ;

main
