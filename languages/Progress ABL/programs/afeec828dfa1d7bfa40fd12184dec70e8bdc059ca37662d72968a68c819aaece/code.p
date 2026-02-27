DEFINE VARIABLE i AS INTEGER NO-UNDO.

DO i = 1 TO 100:
    IF i MODULO 15 = 0 THEN
        MESSAGE "FizzBuzz".
    ELSE IF i MODULO 3 = 0 THEN
        MESSAGE "Fizz".
    ELSE IF i MODULO 5 = 0 THEN
        MESSAGE "Buzz".
    ELSE
        MESSAGE i.
END.
