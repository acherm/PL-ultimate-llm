REM Fibonacci sequence generator in Turbo BASIC
CLS
INPUT "How many Fibonacci numbers to generate"; N%
A% = 0
B% = 1
PRINT A%
PRINT B%
FOR I% = 3 TO N%
    C% = A% + B%
    PRINT C%
    A% = B%
    B% = C%
NEXT I%
END
