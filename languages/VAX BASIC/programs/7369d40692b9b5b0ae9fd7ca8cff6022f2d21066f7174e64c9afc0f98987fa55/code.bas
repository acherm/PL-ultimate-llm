PROGRAM FIBONACCI
! Fibonacci sequence calculator in VAX BASIC
! Computes and displays Fibonacci numbers up to a limit

DECLARE INTEGER N, A, B, TEMP, COUNT, LIMIT

LIMIT = 10
A = 0
B = 1
COUNT = 0

PRINT "Fibonacci sequence:"
PRINT A

WHILE COUNT < LIMIT
    PRINT B
    TEMP = A + B
    A = B
    B = TEMP
    COUNT = COUNT + 1
NEXT

END PROGRAM
