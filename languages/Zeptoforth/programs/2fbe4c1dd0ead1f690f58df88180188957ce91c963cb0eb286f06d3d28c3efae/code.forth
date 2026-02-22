\ Calculate Fibonacci numbers recursively

: fib ( n -- result )
  dup 2 < if
    drop 1
  else
    dup 1- recurse
    swap 2 - recurse
    +
  then ;

\ Print first 10 Fibonacci numbers
: main ( -- )
  11 0 do
    i fib .
  loop
  cr ;

main
