' Fibonacci sequence calculator in X11-Basic
PRINT "Fibonacci Sequence Calculator"
PRINT "Enter the number of terms: "
INPUT n
IF n < 1 THEN
  PRINT "Please enter a positive number"
  QUIT
ENDIF
a = 0
b = 1
PRINT "Fibonacci sequence:"
FOR i = 1 TO n
  PRINT a;
  IF i < n THEN PRINT ", ";
  temp = a + b
  a = b
  b = temp
NEXT i
PRINT
PRINT "Done!"
