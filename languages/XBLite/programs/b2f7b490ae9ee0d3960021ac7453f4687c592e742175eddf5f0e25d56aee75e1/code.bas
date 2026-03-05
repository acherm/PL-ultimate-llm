' XBLite - Fibonacci sequence example

FUNCTION Fibonacci(n AS INT) AS INT
  IF n < 2 THEN
    RETURN n
  END IF
  RETURN Fibonacci(n - 1) + Fibonacci(n - 2)
END FUNCTION

DIM i AS INT
FOR i = 0 TO 10
  PRINT i, Fibonacci(i)
NEXT i
