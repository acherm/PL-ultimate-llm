REM Factorial Calculator in ZBASIC
DIM n AS INTEGER, fact AS LONG
INPUT "Enter a number: ", n
fact = 1
FOR i = 1 TO n
    fact = fact * i
NEXT i
PRINT n; "! = "; fact
