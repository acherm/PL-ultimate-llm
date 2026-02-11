' Fibonacci sequence generator in ScriptBasic
' Calculates and displays the first N Fibonacci numbers

DECLARE SUB Fibonacci(n)

n = 15
PRINT "First ", n, " Fibonacci numbers:\n"
Fibonacci(n)

SUB Fibonacci(count)
  LOCAL a, b, temp, i
  
  a = 0
  b = 1
  
  FOR i = 1 TO count
    PRINT a, " "
    temp = a + b
    a = b
    b = temp
  NEXT i
  
  PRINT "\n"
END SUB
