$APPTYPE CONSOLE

DECLARE SUB Fibonacci (n AS INTEGER)

SUB Fibonacci (n AS INTEGER)
    DIM a AS INTEGER, b AS INTEGER, c AS INTEGER, i AS INTEGER
    a = 0
    b = 1
    PRINT "Fibonacci sequence up to "; n; " terms:"
    FOR i = 1 TO n
        PRINT a;
        c = a + b
        a = b
        b = c
    NEXT i
    PRINT
END SUB

Fibonacci(10)
