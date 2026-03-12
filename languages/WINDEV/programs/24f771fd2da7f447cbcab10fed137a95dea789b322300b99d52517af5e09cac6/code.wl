// Fibonacci sequence in WLanguage (WINDEV)
FUNCTION Fibonacci(n is int) : int
    IF n <= 1 THEN
        RETURN n
    END
    RETURN Fibonacci(n - 1) + Fibonacci(n - 2)

// Display the first 10 Fibonacci numbers
FOR i = 0 TO 9
    Trace("Fib(" + i + ") = " + Fibonacci(i))
END
