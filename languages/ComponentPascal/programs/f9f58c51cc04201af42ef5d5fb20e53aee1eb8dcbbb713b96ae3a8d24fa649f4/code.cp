MODULE Fibonacci;

	IMPORT Out;

	PROCEDURE Fib(n: INTEGER): INTEGER;
	BEGIN
		IF n <= 1 THEN
			RETURN n
		ELSE
			RETURN Fib(n-1) + Fib(n-2)
		END
	END Fib;

	VAR i: INTEGER;

BEGIN
	FOR i := 0 TO 10 DO
		Out.Int(Fib(i), 0); Out.String(' ')
	END;
	Out.Ln
END Fibonacci.
