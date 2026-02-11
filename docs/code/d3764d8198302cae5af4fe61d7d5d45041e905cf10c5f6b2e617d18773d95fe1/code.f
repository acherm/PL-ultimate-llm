      PROGRAM FACTORIAL
      INTEGER N, FACT, I
      PRINT *, 'ENTER A NUMBER:'
      READ *, N
      FACT = 1
      DO 10 I = 1, N
         FACT = FACT * I
   10 CONTINUE
      PRINT *, 'FACTORIAL OF', N, 'IS', FACT
      STOP
      END