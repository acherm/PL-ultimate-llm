: fib ( n -- fib_n )
  dup 2 < if drop 1 exit then
  dup  1 - recurse
  swap 2 - recurse + ;

: .fibs ( n -- )
  1+ 1 do i fib . loop ;

10 .fibs
