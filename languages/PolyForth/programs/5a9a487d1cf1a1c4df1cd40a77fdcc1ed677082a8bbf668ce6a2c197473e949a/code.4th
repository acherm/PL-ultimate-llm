: SQUARE  ( n -- n^2 )  DUP * ;

: CUBE  ( n -- n^3 )  DUP SQUARE * ;

: .SQUARES  ( n -- )
  1 DO
    I SQUARE .
  LOOP ;

10 .SQUARES