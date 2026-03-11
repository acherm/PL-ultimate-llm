* FizzBuzz in dBASE III
SET TALK OFF
SET ECHO OFF
STORE 1 TO n
DO WHILE n <= 100
  IF MOD(n, 15) = 0
    ? "FizzBuzz"
  ELSE
    IF MOD(n, 3) = 0
      ? "Fizz"
    ELSE
      IF MOD(n, 5) = 0
        ? "Buzz"
      ELSE
        ? n
      ENDIF
    ENDIF
  ENDIF
  STORE n + 1 TO n
ENDDO
