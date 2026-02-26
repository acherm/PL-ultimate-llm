: FIBONACCI ( n -- fib )
    DUP 2 < IF EXIT THEN
    DUP 1- RECURSE
    SWAP 2- RECURSE
    + ;

: .FIBS ( n -- )
    1+ 0 SWAP DO
        I FIBONACCI .
    LOOP ;

10 .FIBS
