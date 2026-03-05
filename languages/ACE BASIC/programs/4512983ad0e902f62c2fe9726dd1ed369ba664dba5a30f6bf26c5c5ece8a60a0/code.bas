' Fibonacci sequence in ACE BASIC
' Computes and prints Fibonacci numbers up to index 20

DIM fib(20)

fib(0) = 0
fib(1) = 1

FOR i = 2 TO 20
  fib(i) = fib(i-1) + fib(i-2)
NEXT i

FOR i = 0 TO 20
  PRINT "fib("; i; ") = "; fib(i)
NEXT i
