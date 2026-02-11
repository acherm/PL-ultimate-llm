10 REM Business BASIC Program - Sum of Numbers
20 PRINT "Enter how many numbers to sum:"
30 INPUT N
40 LET S = 0
50 FOR I = 1 TO N
60 PRINT "Enter number"; I; ":"
70 INPUT X
80 LET S = S + X
90 NEXT I
100 PRINT "The sum is:"; S
110 END
