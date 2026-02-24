PROCEDURE Main()
   LOCAL i
   FOR i := 1 TO 100
      IF i % 15 == 0
         ? "FizzBuzz"
      ELSEIF i % 3 == 0
         ? "Fizz"
      ELSEIF i % 5 == 0
         ? "Buzz"
      ELSE
         ? i
      ENDIF
   NEXT
RETURN