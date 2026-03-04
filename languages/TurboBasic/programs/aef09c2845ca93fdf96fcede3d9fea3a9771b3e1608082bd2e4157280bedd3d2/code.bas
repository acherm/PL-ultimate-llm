' TurboBasic: Prime number sieve
DEFINT A-Z
DIM sieve(100)
n = 100

FOR i = 2 TO n
    sieve(i) = 1
NEXT i

FOR i = 2 TO INT(SQR(n))
    IF sieve(i) = 1 THEN
        FOR j = i*i TO n STEP i
            sieve(j) = 0
        NEXT j
    END IF
NEXT i

PRINT "Primes up to"; n; ":"
FOR i = 2 TO n
    IF sieve(i) = 1 THEN PRINT i;
NEXT i
PRINT
END
