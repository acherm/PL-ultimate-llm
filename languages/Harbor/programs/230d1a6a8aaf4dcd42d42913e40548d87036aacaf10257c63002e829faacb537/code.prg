// Fibonacci sequence in Harbor
FUNCTION Fibonacci( n )
   IF n <= 1
      RETURN n
   ENDIF
   RETURN Fibonacci( n - 1 ) + Fibonacci( n - 2 )

PROCEDURE Main()
   LOCAL i
   ? "Fibonacci sequence:"
   FOR i := 0 TO 10
      ? "fib(" + Str( i, 2 ) + ") = " + Str( Fibonacci( i ), 4 )
   NEXT
   RETURN
