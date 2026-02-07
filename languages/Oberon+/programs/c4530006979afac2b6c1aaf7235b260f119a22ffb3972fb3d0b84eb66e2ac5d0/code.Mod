MODULE Fibonacci;
  IMPORT Out;

  PROCEDURE Fib(n: INTEGER): INTEGER;
  VAR a, b, temp, i: INTEGER;
  BEGIN
    a := 0;
    b := 1;
    i := 0;
    WHILE i < n DO
      temp := a + b;
      a := b;
      b := temp;
      INC(i);
    END;
    RETURN a;
  END Fib;

BEGIN
  Out.String("Fibonacci(10) = ");
  Out.Int(Fib(10), 0);
  Out.Ln;
END Fibonacci.
