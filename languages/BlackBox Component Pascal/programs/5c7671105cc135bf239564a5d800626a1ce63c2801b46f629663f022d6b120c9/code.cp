MODULE Fibonacci;

  IMPORT StdLog;

  PROCEDURE Fib (n: INTEGER): INTEGER;
  BEGIN
    IF n <= 1 THEN RETURN n
    ELSE RETURN Fib(n - 1) + Fib(n - 2)
    END
  END Fib;

  PROCEDURE Do*;
    VAR i: INTEGER;
  BEGIN
    FOR i := 0 TO 10 DO
      StdLog.Int(Fib(i), 0);
      StdLog.Char(' ')
    END;
    StdLog.Ln
  END Do;

END Fibonacci.
