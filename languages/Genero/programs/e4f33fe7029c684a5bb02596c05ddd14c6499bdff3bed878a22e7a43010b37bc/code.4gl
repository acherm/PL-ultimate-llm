MAIN
    DEFINE n, a, b, tmp INTEGER

    LET a = 0
    LET b = 1
    DISPLAY "Fibonacci sequence:"
    FOR n = 1 TO 15
        DISPLAY a
        LET tmp = a + b
        LET a = b
        LET b = tmp
    END FOR
END MAIN
