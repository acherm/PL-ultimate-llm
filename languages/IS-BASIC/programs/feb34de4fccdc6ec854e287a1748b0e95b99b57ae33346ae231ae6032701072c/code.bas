100 ! Prime Number Finder
110 ! Find and display prime numbers up to a limit
120 !
130 INPUT PROMPT "Enter upper limit: ":LIMIT
140 PRINT "Prime numbers up to";LIMIT;":"
150 FOR N=2 TO LIMIT
160   LET ISPRIME=1
170   FOR I=2 TO INT(SQR(N))
180     IF N MOD I=0 THEN LET ISPRIME=0:EXIT FOR
190   NEXT I
200   IF ISPRIME=1 THEN PRINT N;
210 NEXT N
220 PRINT
230 END