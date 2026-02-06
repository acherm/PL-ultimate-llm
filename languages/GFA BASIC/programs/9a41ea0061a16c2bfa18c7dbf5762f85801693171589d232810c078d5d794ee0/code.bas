' Fibonacci sequence calculator
' GFA BASIC program
'
DIM fib(20)
CLS
PRINT "Fibonacci Sequence"
PRINT
fib(0) = 0
fib(1) = 1
PRINT "F(0) = "; fib(0)
PRINT "F(1) = "; fib(1)
FOR i% = 2 TO 15
  fib(i%) = fib(i%-1) + fib(i%-2)
  PRINT "F("; i%; ") = "; fib(i%)
NEXT i%
'
' Wait for keypress
DO
EXIT IF INKEY$ <> ""
LOOP
