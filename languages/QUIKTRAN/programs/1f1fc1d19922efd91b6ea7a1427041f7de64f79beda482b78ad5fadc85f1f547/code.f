C     FACTORIAL CALCULATOR IN QUIKTRAN
      INTEGER N, I, FACT
      FACT = 1
      N = 5
      DO 10 I = 1, N
         FACT = FACT * I
   10 CONTINUE
      WRITE(6,20) N, FACT
   20 FORMAT(1X, 'FACTORIAL OF ', I2, ' IS ', I10)
      STOP
      END
