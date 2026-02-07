FUNCTION FibonacciIterative(n AS LONG) AS LONG
    DIM a AS LONG, b AS LONG, temp AS LONG, i AS LONG
    a = 0
    b = 1
    IF n = 0 THEN
        FUNCTION = 0
        EXIT FUNCTION
    END IF
    FOR i = 2 TO n
        temp = a + b
        a = b
        b = temp
    NEXT i
    FUNCTION = b
END FUNCTION

FUNCTION PBMAIN() AS LONG
    DIM result AS LONG, i AS LONG
    FOR i = 0 TO 10
        result = FibonacciIterative(i)
        PRINT "Fibonacci(" & STR$(i) & ") = " & STR$(result)
    NEXT i
    WAITKEY$
    FUNCTION = 0
END FUNCTION
