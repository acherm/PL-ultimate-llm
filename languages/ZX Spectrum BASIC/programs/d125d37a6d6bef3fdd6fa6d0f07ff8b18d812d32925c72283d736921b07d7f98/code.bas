10 REM Mandelbrot Set Generator
20 LET xmin = -2.5
30 LET xmax = 1
40 LET ymin = -1
50 LET ymax = 1
60 LET maxiter = 16
70 FOR py = 0 TO 175
80 LET y0 = ymin + (ymax - ymin) * py / 175
90 FOR px = 0 TO 255
100 LET x0 = xmin + (xmax - xmin) * px / 255
110 LET x = 0
120 LET y = 0
130 LET iteration = 0
140 IF x * x + y * y > 4 THEN GOTO 200
150 IF iteration >= maxiter THEN GOTO 200
160 LET xtemp = x * x - y * y + x0
170 LET y = 2 * x * y + y0
180 LET x = xtemp
190 LET iteration = iteration + 1: GOTO 140
200 IF iteration < maxiter THEN PLOT px, py
210 NEXT px
220 NEXT py
