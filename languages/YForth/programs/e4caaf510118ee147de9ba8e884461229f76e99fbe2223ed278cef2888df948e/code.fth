\ == recursive version ==

: fib
dup 2 <= if
drop 1
else
dup 1 - recurse
swap 2 - recurse +
then ;

\ using:

10 fib .

\ == end of script ==
