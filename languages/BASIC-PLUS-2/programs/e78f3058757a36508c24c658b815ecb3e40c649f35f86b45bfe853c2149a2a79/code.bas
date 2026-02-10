10 REM Fibonacci Number Generator in BASIC-PLUS-2
20 DECLARE INTEGER N, I, FIB1, FIB2, TEMP
30 PRINT "Enter the number of Fibonacci numbers to generate: ";
40 INPUT N
50 IF N < 1 THEN
60     PRINT "Please enter a positive number"
70     GOTO 30
80 END IF
90 FIB1 = 0
100 FIB2 = 1
110 PRINT "Fibonacci sequence:"
120 PRINT FIB1
130 IF N > 1 THEN PRINT FIB2
140 FOR I = 3 TO N
150     TEMP = FIB1 + FIB2
160     PRINT TEMP
170     FIB1 = FIB2
180     FIB2 = TEMP
190 NEXT I
200 END