100 PRINT "Quadratic Equation Solver"
110 PRINT "Solves ax^2 + bx + c = 0"
120 PRINT
130 INPUT "Enter coefficient a: ", A
140 INPUT "Enter coefficient b: ", B
150 INPUT "Enter coefficient c: ", C
160 LET D = B * B - 4 * A * C
170 IF D < 0 THEN 250
180 IF D = 0 THEN 220
190 LET X1 = (-B + SQR(D)) / (2 * A)
200 LET X2 = (-B - SQR(D)) / (2 * A)
210 PRINT "Two roots: x1 ="; X1; ", x2 ="; X2
215 GOTO 260
220 LET X = -B / (2 * A)
230 PRINT "One root: x ="; X
240 GOTO 260
250 PRINT "No real roots (discriminant is negative)"
260 END
