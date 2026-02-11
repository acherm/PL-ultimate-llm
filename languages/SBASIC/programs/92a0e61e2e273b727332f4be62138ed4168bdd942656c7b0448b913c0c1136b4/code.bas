100 REM Fibonacci Number Generator
110 REM Data General SBASIC Example
120 PRINT "Fibonacci Number Generator"
130 PRINT "How many numbers to generate";
140 INPUT N
150 IF N < 1 THEN 130
160 LET A = 0
170 LET B = 1
180 PRINT A
190 IF N = 1 THEN 280
200 PRINT B
210 IF N = 2 THEN 280
220 FOR I = 3 TO N
230   LET C = A + B
240   PRINT C
250   LET A = B
260   LET B = C
270 NEXT I
280 PRINT "Done"
290 END
