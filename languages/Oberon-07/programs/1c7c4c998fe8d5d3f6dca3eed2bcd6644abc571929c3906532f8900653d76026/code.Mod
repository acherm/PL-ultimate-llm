MODULE Fibonacci;
  IMPORT Out;
  
  PROCEDURE Calc(n: INTEGER): INTEGER;
    VAR a, b, i, temp: INTEGER;
  BEGIN
    a := 0; b := 1;
    FOR i := 1 TO n DO
      temp := a + b;
      a := b;
      b := temp
    END;
    RETURN a
  END Calc;
  
  PROCEDURE Run*;
    VAR i: INTEGER;
  BEGIN
    FOR i := 0 TO 10 DO
      Out.Int(i, 4);
      Out.String(": ");
      Out.Int(Calc(i), 8);
      Out.Ln
    END
  END Run;
  
BEGIN
  Run
END Fibonacci.
