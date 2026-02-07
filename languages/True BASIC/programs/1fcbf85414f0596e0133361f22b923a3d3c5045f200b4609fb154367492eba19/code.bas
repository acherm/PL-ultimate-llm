! Fibonacci sequence generator
! True BASIC program

OPTION NOLET
DIM fib(20)

LET fib(1) = 0
LET fib(2) = 1

PRINT "Fibonacci Sequence:"
PRINT fib(1)
PRINT fib(2)

FOR i = 3 TO 20
    LET fib(i) = fib(i-1) + fib(i-2)
    PRINT fib(i)
NEXT i

END
