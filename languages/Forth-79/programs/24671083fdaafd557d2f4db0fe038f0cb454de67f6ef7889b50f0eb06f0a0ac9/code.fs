: fib ( n -- fib )
    dup 2 < if exit then
    dup  1- recurse
    swap 2- recurse  + ;

20 fib . cr
