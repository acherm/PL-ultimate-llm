! Sieve of Eratosthenes in Full BASIC
! ANSI Full BASIC (X3.113-1987)

PROGRAM Sieve

LET limit = 100
DIM flag(limit)

FOR i = 2 TO limit
    LET flag(i) = 1
NEXT i

FOR i = 2 TO INT(SQR(limit))
    IF flag(i) = 1 THEN
        LET j = i * i
        DO WHILE j <= limit
            LET flag(j) = 0
            LET j = j + i
        LOOP
    END IF
NEXT i

PRINT "Primes up to"; limit
FOR i = 2 TO limit
    IF flag(i) = 1 THEN PRINT i;
NEXT i
PRINT

END
