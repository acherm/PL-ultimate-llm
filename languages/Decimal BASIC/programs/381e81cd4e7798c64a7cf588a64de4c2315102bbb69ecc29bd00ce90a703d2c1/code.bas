FOR n = 1 TO 100
    IF MOD(n, 15) = 0 THEN
        PRINT "FizzBuzz"
    ELSEIF MOD(n, 3) = 0 THEN
        PRINT "Fizz"
    ELSEIF MOD(n, 5) = 0 THEN
        PRINT "Buzz"
    ELSE
        PRINT n
    END IF
NEXT n
END
