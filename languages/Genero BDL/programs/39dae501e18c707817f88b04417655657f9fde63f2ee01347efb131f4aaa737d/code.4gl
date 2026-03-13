MAIN
    DEFINE i INTEGER
    DEFINE a, b, temp INTEGER

    LET a = 0
    LET b = 1
    DISPLAY "Fibonacci sequence:"
    FOR i = 1 TO 10
        DISPLAY a
        LET temp = a + b
        LET a = b
        LET b = temp
    END FOR
END MAIN
