: fib ( n -- fib )
    dup 2 < if drop 1 exit then
    dup 1- recurse swap 2- recurse + ;

: .fibs ( n -- )
    0 do
        i fib . space
    loop cr ;

10 .fibs
