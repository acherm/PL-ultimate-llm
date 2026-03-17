* Fibonacci sequence example in Recital
* Demonstrates recursive functions and output

FUNCTION fibonacci(n)
   IF n <= 1
      RETURN n
   ENDIF
   RETURN fibonacci(n-1) + fibonacci(n-2)
ENDFUNC

* Main program
LOCAL i
FOR i = 0 TO 10
   ? "fibonacci(" + LTRIM(STR(i)) + ") = " + LTRIM(STR(fibonacci(i)))
NEXT
