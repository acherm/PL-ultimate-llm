10 REM Prime Number Generator
20 REM MBASIC Program to find prime numbers up to N
30 PRINT "Prime Number Generator"
40 PRINT
50 INPUT "Enter maximum number: ", N
60 IF N < 2 THEN PRINT "No primes less than 2": GOTO 200
70 PRINT "Prime numbers up to"; N; ":"
80 PRINT
90 FOR I = 2 TO N
100   ISPRIME = 1
110   IF I > 2 THEN IF I MOD 2 = 0 THEN ISPRIME = 0: GOTO 170
120   LIMIT = INT(SQR(I))
130   FOR J = 3 TO LIMIT STEP 2
140     IF I MOD J = 0 THEN ISPRIME = 0: GOTO 160
150   NEXT J
160   REM Check if prime flag is still set
170   IF ISPRIME = 1 THEN PRINT I
180 NEXT I
190 PRINT
200 END