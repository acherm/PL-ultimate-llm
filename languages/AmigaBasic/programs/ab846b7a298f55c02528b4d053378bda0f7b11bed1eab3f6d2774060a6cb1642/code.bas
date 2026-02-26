' FizzBuzz in AmigaBasic
FOR n% = 1 TO 20
    s$ = ""
    IF (n% MOD 3) = 0 THEN s$ = s$ + "Fizz"
    IF (n% MOD 5) = 0 THEN s$ = s$ + "Buzz"
    IF s$ = "" THEN s$ = STR$(n%)
    PRINT s$
NEXT n%
