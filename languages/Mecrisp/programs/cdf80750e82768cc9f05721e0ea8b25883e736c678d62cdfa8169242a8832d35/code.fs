: factorial ( n -- n! )
  dup 1 > if
    dup 1- recurse *
  then
;

: test-factorial ( -- )
  cr ." Factorial tests:" cr
  6 0 do
    i dup factorial
    ." " i . ." ! = " . cr
  loop
;

test-factorial
