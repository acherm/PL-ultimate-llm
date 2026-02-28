10 REM Fibonacci sequence
20 LET a = 0
30 LET b = 1
40 LET count = 10
50 IF count = 0 THEN GOTO 100
60 PRINT STR(a)
70 LET tmp = b
80 LET b = a + b
90 LET a = tmp
95 LET count = count - 1
96 GOTO 50
100 END
