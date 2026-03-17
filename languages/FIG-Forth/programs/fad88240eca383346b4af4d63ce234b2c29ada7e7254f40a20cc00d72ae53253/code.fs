: FACT ( n -- n! )
  DUP 2 < IF DROP 1 EXIT THEN
  DUP 1- RECURSE * ;

: .FACTS ( n -- )
  1+ 1 DO
    I . ." ! = " I FACT . CR
  LOOP ;

." Factorials 1 to 7:" CR
7 .FACTS