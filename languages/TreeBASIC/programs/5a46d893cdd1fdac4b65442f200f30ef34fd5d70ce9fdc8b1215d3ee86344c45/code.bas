SUB main()
    DIM message AS STRING
    DIM i AS INTEGER

    message = "Hello from TreeBASIC!"
    PRINT message

    PRINT "Counting to 10:"
    FOR i = 1 TO 10
        PRINT i
    NEXT i

    PRINT "Fibonacci sequence:"
    CALL ShowFibonacci(10)
END SUB

SUB ShowFibonacci(n AS INTEGER)
    DIM a AS INTEGER
    DIM b AS INTEGER
    DIM temp AS INTEGER
    DIM i AS INTEGER

    a = 0
    b = 1

    FOR i = 1 TO n
        PRINT a
        temp = a + b
        a = b
        b = temp
    NEXT i
END SUB