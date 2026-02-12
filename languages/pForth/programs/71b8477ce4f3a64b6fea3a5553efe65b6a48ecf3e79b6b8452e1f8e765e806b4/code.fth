\ Fibonacci number calculator in pForth
\ Prints the first 15 Fibonacci numbers

: fib ( n -- fib[n] )
  dup 2 < if
    drop 1
  else
    dup 1 - recurse
    swap 2 - recurse +
  then ;

: print-fibs ( n -- )
  0 do
    i fib . cr
  loop ;

\ Main program
." First 15 Fibonacci numbers:" cr
15 print-fibs
