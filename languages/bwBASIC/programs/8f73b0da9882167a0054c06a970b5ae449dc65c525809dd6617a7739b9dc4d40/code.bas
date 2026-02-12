10 REM Prime Number Generator in bwBASIC
20 REM Finds and displays prime numbers up to a limit
30 PRINT "Prime Number Generator"
40 PRINT "Enter upper limit: ";
50 INPUT LIMIT
60 IF LIMIT < 2 THEN
70   PRINT "Limit must be at least 2"
80   GOTO 40
90 END IF
100 PRINT "Prime numbers up to"; LIMIT; ":"
110 FOR N = 2 TO LIMIT
120   LET ISPRIME = 1
130   FOR I = 2 TO INT(SQR(N))
140     IF N MOD I = 0 THEN
150       LET ISPRIME = 0
160       GOTO 180
170     END IF
180   NEXT I
190   IF ISPRIME = 1 THEN PRINT N;
200 NEXT N
210 PRINT
220 END
