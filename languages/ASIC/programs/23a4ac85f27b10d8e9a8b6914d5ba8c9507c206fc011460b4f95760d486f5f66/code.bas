REM Fibonacci Sequence Generator in ASIC
DIM fib(20)
fib(0) = 0
fib(1) = 1
PRINT "Fibonacci sequence:"
PRINT fib(0)
PRINT fib(1)
FOR i = 2 TO 15
    fib(i) = fib(i-1) + fib(i-2)
    PRINT fib(i)
NEXT i
END