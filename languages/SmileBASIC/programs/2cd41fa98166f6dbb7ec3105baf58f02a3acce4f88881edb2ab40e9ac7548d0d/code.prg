'Fibonacci Sequence Generator
CLS
PRINT "Fibonacci Sequence Generator"
PRINT "Enter how many terms: ";
INPUT N

A = 0
B = 1

FOR I = 1 TO N
  PRINT A;
  C = A + B
  A = B
  B = C
NEXT

PRINT
PRINT "Done!"
