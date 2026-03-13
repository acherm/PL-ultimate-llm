' Fibonacci sequence in TBasic
DIM a AS INTEGER
DIM b AS INTEGER
DIM c AS INTEGER

a = 0
b = 1
PRINT "Fibonacci Sequence (first 15 terms):"
FOR i = 1 TO 15
    PRINT a
    c = a + b
    a = b
    b = c
NEXT i
END
