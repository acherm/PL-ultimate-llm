-- Factorial function in Cedar
-- Computes factorial recursively

Factorial: CEDAR PROGRAM
  IMPORTS IO
  = BEGIN

  Fac: PROC [n: INT] RETURNS [INT] = {
    IF n <= 1 THEN RETURN [1]
    ELSE RETURN [n * Fac[n-1]];
  };

  -- Main program
  result: INT;
  result <- Fac[5];
  IO.PutF["Factorial of 5 is %g\n", [integer[result]]];

  END.
