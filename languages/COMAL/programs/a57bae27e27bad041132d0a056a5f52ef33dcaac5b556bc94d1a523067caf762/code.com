// Towers of Hanoi
//
// UniComal
//
// 1999-03-24

PAGE
discs:=0
REPEAT
  PRINT "How many discs";
  INPUT discs
UNTIL discs>0 AND discs<10

CLS
from:=1
to:=3
via:=2
PROC hanoi(discs,from,to,via)
ENDPAGE

PROC hanoi(d,f,t,v)
  IF d>0 THEN
    PROC hanoi(d-1,f,v,t)
    PRINT "Move disc ";d;" from ";f;" to ";t
    PROC hanoi(d-1,v,t,f)
  ENDIF
ENDPROC hanoi