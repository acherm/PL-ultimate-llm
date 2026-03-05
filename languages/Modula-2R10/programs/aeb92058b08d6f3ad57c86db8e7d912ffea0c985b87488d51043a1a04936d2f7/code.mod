MODULE Fibonacci;

FROM InOut IMPORT WriteCard, WriteLn;

PROCEDURE Fib ( n : CARDINAL ) : CARDINAL;
BEGIN
  IF n <= 1 THEN
    RETURN n
  ELSE
    RETURN Fib(n-1) + Fib(n-2)
  END (* IF *)
END Fib;

VAR
  i : CARDINAL;

BEGIN
  FOR i := 0 TO 10 DO
    WriteCard(Fib(i), 6);
    WriteLn
  END (* FOR *)
END Fibonacci.
