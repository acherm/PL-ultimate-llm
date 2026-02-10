REM Fibonacci sequence generator
INPUT "How many Fibonacci numbers? ", n
a = 0
b = 1
FOR i = 1 TO n
  PRINT a;
  c = a + b
  a = b
  b = c
NEXT i
PRINT
