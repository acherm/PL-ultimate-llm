BEGIN
   COMMENT Sample B6700 Algol Program - Factorial Calculation;
   INTEGER I, N, RESULT;

   PROCEDURE FACTORIAL(N);
   VALUE N;
   INTEGER N;
   BEGIN
      INTEGER I, FACT;
      FACT := 1;
      FOR I := 1 STEP 1 UNTIL N DO
         FACT := FACT * I;
      FACTORIAL := FACT
   END FACTORIAL;

   N := 5;
   RESULT := FACTORIAL(N);
   WRITE(TEXT("FACTORIAL OF "), N, TEXT(" IS "), RESULT)
END