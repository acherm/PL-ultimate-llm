! Fibonacci sequence in True BASIC
! Computes and prints the first 15 Fibonacci numbers

LET a = 0
LET b = 1
PRINT "Fibonacci sequence:"
FOR i = 1 TO 15
    PRINT a;
    LET temp = a + b
    LET a = b
    LET b = temp
NEXT i
PRINT
END
