FOR i = 1 TO 100
    DO CASE
        CASE MOD(i, 15) = 0
            ? "FizzBuzz"
        CASE MOD(i, 3) = 0
            ? "Fizz"
        CASE MOD(i, 5) = 0
            ? "Buzz"
        OTHERWISE
            ? LTRIM(STR(i))
    ENDCASE
ENDFOR
