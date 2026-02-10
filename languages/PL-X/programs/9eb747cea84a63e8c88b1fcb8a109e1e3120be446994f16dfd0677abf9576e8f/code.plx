/* Factorial calculation in PL/X */
FACTORIAL: PROC(N) RETURNS(FIXED);
   DCL N FIXED;
   DCL I FIXED;
   DCL RESULT FIXED;

   IF N <= 1 THEN
      RETURN(1);

   RESULT = 1;
   DO I = 2 TO N;
      RESULT = RESULT * I;
   END;

   RETURN(RESULT);
END FACTORIAL;

/* Test the factorial function */
MAIN: PROC;
   DCL NUM FIXED;
   DCL FACT FIXED;

   NUM = 5;
   FACT = FACTORIAL(NUM);

   /* Display result */
   CALL DISPLAY('FACTORIAL OF ' || NUM || ' IS ' || FACT);
END MAIN;
