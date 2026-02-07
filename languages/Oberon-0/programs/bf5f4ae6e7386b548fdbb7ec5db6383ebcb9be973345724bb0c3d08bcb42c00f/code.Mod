MODULE Factorial;
  PROCEDURE Calculate*(n: INTEGER): INTEGER;
    VAR result: INTEGER;
  BEGIN
    IF n <= 1 THEN
      result := 1
    ELSE
      result := n * Calculate(n - 1)
    END;
    RETURN result
  END Calculate;
END Factorial.
