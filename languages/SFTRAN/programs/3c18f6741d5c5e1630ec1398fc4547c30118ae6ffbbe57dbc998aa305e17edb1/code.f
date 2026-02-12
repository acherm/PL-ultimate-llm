      PROGRAM FACT
      INTEGER N, I, RESULT
      WRITE(6,*) 'ENTER A NUMBER:'
      READ(5,*) N
      RESULT = 1
      DO I = 1, N
         RESULT = RESULT * I
      END DO
      WRITE(6,*) 'FACTORIAL IS:', RESULT
      STOP
      END