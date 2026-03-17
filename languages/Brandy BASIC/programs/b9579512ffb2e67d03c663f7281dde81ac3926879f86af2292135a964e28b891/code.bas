   10 REM Sieve of Eratosthenes in Brandy BASIC
   20 LIMIT% = 100
   30 DIM sieve%(LIMIT%)
   40 FOR i% = 2 TO LIMIT%
   50   IF sieve%(i%) = 0 THEN
   60     PRINT i%
   70     FOR j% = i%*2 TO LIMIT% STEP i%
   80       sieve%(j%) = 1
   90     NEXT j%
  100   ENDIF
  110 NEXT i%
