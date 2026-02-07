10 REM Spiral Pattern
20 CLS
30 LET x = 128
40 LET y = 88
50 LET a = 0
60 LET r = 0
70 FOR i = 1 TO 500
80 LET r = r + 0.5
90 LET a = a + 0.1
100 LET nx = x + r * COS a
110 LET ny = y + r * SIN a
120 PLOT nx, ny
130 NEXT i
140 PAUSE 0