* Simple Fibonacci sequence generator
PROGRAM FIBONACCI
DIM FIB(20)
FIB(1) = 1
FIB(2) = 1
PRINT "Fibonacci Sequence:"
PRINT FIB(1)
PRINT FIB(2)
FOR I = 3 TO 20
   FIB(I) = FIB(I-1) + FIB(I-2)
   PRINT FIB(I)
NEXT I
END
