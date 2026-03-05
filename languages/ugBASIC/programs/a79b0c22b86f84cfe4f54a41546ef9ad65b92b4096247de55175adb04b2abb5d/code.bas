DIM a AS INTEGER
DIM b AS INTEGER
DIM c AS INTEGER
DIM i AS INTEGER

a = 0
b = 1
PRINT a
PRINT b
FOR i = 0 TO 7
  c = a + b
  PRINT c
  a = b
  b = c
NEXT i
