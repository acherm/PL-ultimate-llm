PROGRAM Fibonacci

; PROMAL program to calculate Fibonacci numbers
; Demonstrates structured programming with procedures

CONST
  MAX = 10

VAR
  i, n1, n2, next: INTEGER

PROC PrintFib(count: INTEGER)
  LOCAL i, n1, n2, next: INTEGER
  
  n1 = 0
  n2 = 1
  
  PRINT("Fibonacci Series up to ", count, " terms:")
  
  FOR i = 1 TO count DO
    IF i = 1 THEN
      PRINT(n1)
      NEXT i
    ENDIF
    
    IF i = 2 THEN
      PRINT(n2)
      NEXT i
    ENDIF
    
    next = n1 + n2
    n1 = n2
    n2 = next
    PRINT(next)
  ENDFOR
END PROC

BEGIN
  PrintFib(MAX)
END
