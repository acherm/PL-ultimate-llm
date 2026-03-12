#AppType Console

FUNCTION Fibonacci(n AS INTEGER) AS INTEGER
    IF n < 2 THEN
        RETURN n
    END IF
    RETURN Fibonacci(n - 1) + Fibonacci(n - 2)
END FUNCTION

DIM i AS INTEGER
FOR i = 0 TO 9
    Print Fibonacci(i)
NEXT

Pause
