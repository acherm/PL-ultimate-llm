10 REM BASIC-80 Prime Number Finder
20 PRINT "Enter a number to check if it is prime:"
30 INPUT N
40 IF N < 2 THEN PRINT N; "is not prime" : GOTO 110
50 IF N = 2 THEN PRINT N; "is prime" : GOTO 110
60 FOR I = 2 TO SQR(N)
70   IF N MOD I = 0 THEN PRINT N; "is not prime (divisible by"; I; ")" : GOTO 110
80 NEXT I
90 PRINT N; "is prime"
110 END
