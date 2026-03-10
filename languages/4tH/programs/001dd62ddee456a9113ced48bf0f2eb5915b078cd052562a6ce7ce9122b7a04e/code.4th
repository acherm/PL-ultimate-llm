: fib ( n -- fib )
  dup 2 < if drop 1 exit then
  dup  1 - recurse
  swap 2 - recurse + ;

: .sequence ( n -- )
  1+ 0 do
    i fib .
  loop
  cr ;

10 .sequence
