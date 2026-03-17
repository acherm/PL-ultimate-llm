FOR I = 1 TO 100
    IF MOD(I, 15) = 0 THEN
        PRINT "FizzBuzz"
    END ELSE
        IF MOD(I, 3) = 0 THEN
            PRINT "Fizz"
        END ELSE
            IF MOD(I, 5) = 0 THEN
                PRINT "Buzz"
            END ELSE
                PRINT I
            END
        END
    END
NEXT I
STOP
