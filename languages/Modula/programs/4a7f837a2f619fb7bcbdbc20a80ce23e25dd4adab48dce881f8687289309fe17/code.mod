MODULE Factorial;
FROM InOut IMPORT WriteString, WriteInt, WriteLn;

VAR n, result: INTEGER;

PROCEDURE Fact(n: INTEGER): INTEGER;
VAR i, f: INTEGER;
BEGIN
  f := 1;
  FOR i := 2 TO n DO
    f := f * i;
  END;
  RETURN f;
END Fact;

BEGIN
  WriteString("Factorial of 5 is: ");
  result := Fact(5);
  WriteInt(result, 0);
  WriteLn;
END Factorial.
