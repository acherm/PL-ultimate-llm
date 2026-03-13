' LBasic - Sieve of Eratosthenes
' Find all prime numbers up to 100

DIM sieve(100)
FOR i = 2 TO 100
    sieve(i) = 1
NEXT i

FOR i = 2 TO 10
    IF sieve(i) = 1 THEN
        FOR j = i*i TO 100 STEP i
            sieve(j) = 0
        NEXT j
    END IF
NEXT i

PRINT "Prime numbers up to 100:"
count = 0
FOR i = 2 TO 100
    IF sieve(i) = 1 THEN
        PRINT i
        count = count + 1
    END IF
NEXT i
PRINT "Total primes found: "; count